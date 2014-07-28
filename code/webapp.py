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

#import pymongo
 
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
load API to load the test data to mongo DB for dashboard
'''

@app.route('/load')
def load():
  
  df = pd.read_csv("../data/test_small.csv")
  print df.head
  impfeatures = ['state','shopping_pt','customer_ID','cost','location','age_youngest','age_oldest','car_age','duration_previous','risk_factor','C_previous','G','group_size']

  print "hello"
  df_test = df[impfeatures]
  df_test = df_test.fillna(method = 'pad')
  df_test['costperperson'] = 1.0 * df.cost/df.group_size

  scores = db.scores
  states = df_test.state.unique()

  for state in states:
    df_test.loc[df_test.state == state,'fscore'] = 0
    df_test.loc[df_test.state == state,'tscore'] = 0
    rec = scores.find_one({'state': state},{'fscore': 1, 'tscore' :1})
    if (rec['fscore']) :
      df_test.loc[df.state == state,'fscore'] = rec['fscore']
    if (rec['tscore']) :
      df_test.loc[df.state == state,'tscore'] = rec['tscore']

  #pdb.set_trace()
  records = json.loads(df_test.T.to_json()).values()
  db.test.remove()
  db.test.insert(records)

 
  return 'Processed all records!!'


'''
 Predict API for predicting the quote conversion
'''
@app.route('/predict')
def predict():

  rec = randint(0,db.test.find().count())
  myObj = db.test.find().limit(-1).skip(rec).next()
  customer_id = str(myObj['customer_ID']) 
  loc = str(myObj['location'])

  df = pd.DataFrame()
  itemlist = []
  collist = []
  for t in myObj.items():
    k,v = t
    collist.append(k)
    itemlist.append(v)

  df = pd.DataFrame(itemlist,collist)
  df = df.T
  df.drop('_id', axis=1, inplace=True)
  df.drop('state', axis=1, inplace=True)
  df.drop('fscore', axis=1, inplace=True)
  df.drop('tscore', axis=1, inplace=True)

  X = np.array(df)
  y_pred = 0
  y_pred_proba= model.predict_proba(X)
  conversion_score = int((y_pred_proba[:,1])*100)
  myObj['conversion_score'] = conversion_score
  myObj['date_time'] = datetime.datetime.now().replace(microsecond=0)
  ## Add test recommendations for now and replace with trained model

  recommendations = db.recs

  rec = recommendations.find_one({'customer_ID': int(customer_id)},{'recommendation1': 1, 'recommendation2' :1})
  print rec 
  myObj['recommendation1'] = rec['recommendation1']
  myObj['recommendation2'] = rec['recommendation2']

  db.analytics.save(myObj)

  html ='<body style="font-family:sans-serif;">'
  html += '<table>'
  html += '<tr>'
  html +='<td>%s </a></td><td align="center" style=\"%s\">%.1f' % (customer_id,loc,conversion_score) + '</td>'
  html += '</tr>'
  html += '</table>'
  html += '</body>'

  return redirect('/dashboard')



'''
Dashboard to check the Quote Status
'''
@app.route('/dashboard')
def dashboard():
  print "Viewing records"
  #pdb.set_trace()
  cur = db.analytics.find().limit(5)
  #cur = db.analytics.find().sort({ datetime.datetime('date_time') : -1 }).limit(8)

  quotes = cur[:10]

  return render_template('dashboard3.html',quotes=quotes)

'''
Flush Dashboard to clean up the old records.
Utility to clean and run the data load again
'''
@app.route('/flush')
def view():
  print "Flushing records"
  db.analytics.remove()
  return "Flushed analytics data!!"


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  model = pickle.load( open( '../model/predict-purchase', 'rb') )

  app.run(host='0.0.0.0', port=port)