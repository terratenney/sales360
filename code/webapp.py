import os
from urlparse import urlparse
from pymongo import Connection
import pdb
import pandas as pd
import pickle
import json
import datetime
from random import randint
import numpy as np
import datetime
from flask import Flask, render_template, request, redirect
import datetime

 
MONGO_URL = os.environ.get('MONGOHQ_URL')
 
if MONGO_URL:
  # Get a connection
  connection = Connection(MONGO_URL)
  # Get the database
  db = connection[urlparse(MONGO_URL).path[1:]]
else:
  # Not on an app with the MongoHQ add-on, do some localhost action
  connection = Connection('localhost', 27017)
  db = connection['customer360']
 
app = Flask(__name__)
app.debug = True
 
'''
load API to load the test data to mongo DB to simulate the realtime inflow quotes in the sales intelligence dashboard
This API is used by web portal admin for a brand new site and data setup. This API will remove any old test data and 
populate a small data set from csv into the mongo db for realtime access. 
'''

@app.route('/load')
def load():
  
  df = pd.read_csv("../data/test_small.csv")

  impfeatures = ['state','shopping_pt','customer_ID','cost','location','age_youngest','age_oldest','car_age','duration_previous','risk_factor','C_previous','G','group_size']


  df_test = df[impfeatures]
  df_test = df_test.fillna(method = 'pad')
  df_test['costperperson'] = 1.0 * df.cost/df.group_size

  scores = db.scores
  states = df_test.state.unique()
  # Load test data along with the scores generated from facebook and twitter.
  # Again the utility of using mongoDB is to replace with Social network siteAdmin data.
  for state in states:
    df_test.loc[df_test.state == state,'fscore'] = 0
    df_test.loc[df_test.state == state,'tscore'] = 0
    rec = scores.find_one({'state': state},{'fscore': 1, 'tscore' :1})
    if (rec['fscore']) :
      df_test.loc[df.state == state,'fscore'] = rec['fscore']
    if (rec['tscore']) :
      df_test.loc[df.state == state,'tscore'] = rec['tscore']

  records = json.loads(df_test.T.to_json()).values()
  db.test.remove()
  db.test.insert(records)

 
  return 'Load Complete  - Processed all records!!'


'''
 Predict API for predicting conversion score based on the quote, this also pulls the recommendations for that customer
 from recommendations database on mongo to provide realtime fast access. Since recommenders are batch and offline processing
 and output is saved to the database for recommendations. Implemented the similar industry approach.
'''
@app.route('/predict')
def predict():

  rec = randint(0,db.test.find().count())
  quote = db.test.find().limit(-1).skip(rec).next()
  customer_id = str(quote['customer_ID']) 
  loc = str(quote['location'])

  df = pd.DataFrame(quote.values(),quote.keys()).transpose()

  df.drop('_id', axis=1, inplace=True)
  df.drop('state', axis=1, inplace=True)
  df.drop('fscore', axis=1, inplace=True)
  df.drop('tscore', axis=1, inplace=True)

  X = np.array(df)
  y_pred_proba= model.predict_proba(X)
  conversion_score = int((y_pred_proba[:,1])*100)
  quote['conversion_score'] = conversion_score
  quote['date_time'] = datetime.datetime.now().replace(microsecond=0)
  ## Add test recommendations for now and replace with trained model

  recommendations = db.recs
  rec = recommendations.find_one({'customer_ID': int(customer_id)},{'recommendation1': 1, 'recommendation2' :1})
  quote['recommendation1'] = rec['recommendation1']
  quote['recommendation2'] = rec['recommendation2']

  db.analytics.save(quote)

  return redirect('/dashboard')



'''
Sales intelligence dashboard to provide the latest top 5 quotes fetched from mongo DB.
analytics collections include conversion score and recommendations.
'''
@app.route('/dashboard')
def dashboard():

  cur = db.analytics.find().sort([("date_time", -1)]).limit(8)

  quotes = cur[:8]

  return render_template('dashboard3.html',quotes=quotes)

'''
Flush Dashboard to clean up the old records.
Utility to clean run backdoor cleanup and run the tests for validations.
Again, this is used by portal admin or developer for testing the data validity on dashboard
'''
@app.route('/flush')
def view():
  print "Flushing records"
  db.analytics.remove()
  return "Flushed analytics data on Dashboard!!"


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  model = pickle.load( open( '../model/predict-purchase', 'rb') )

  app.run(host='0.0.0.0', port=port)