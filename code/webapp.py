import os
from urlparse import urlparse
from flask import Flask
from pymongo import Connection
import pdb
import pandas as pd
import pickle
import json
import datetime
from random import randint
import numpy as np
 
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
def hello():
  
  df = pd.read_csv("../data/test_small.csv")
  print df.head
  impfeatures = ['shopping_pt','customer_ID','cost','location','age_youngest','age_oldest','car_age','duration_previous','risk_factor','C_previous','G','group_size']

  print "hello"
  df_test = df[impfeatures]
  df_test = df_test.fillna(method = 'pad')
  df_test['costperperson'] = 1.0 * df.cost/df.group_size

  #pdb.set_trace()
  records = json.loads(df_test.T.to_json()).values()
  db.test.insert(records)

 
  return 'Processed all records!!'
'''
 Predict API for predicting the quote conversion
'''
@app.route('/predict')
def predict():
  print "Predict Purchase"
  rec = randint(0,db.test.find().count())
  myObj = db.test.find().limit(-1).skip(rec).next()
  #cursor = user_coll.find()
  customer_id = str(myObj['customer_ID']) 
  loc = str(myObj['location'])
  print myObj

  df = pd.DataFrame()
  itemlist = []
  collist = []
  for t in myObj.items():
    k,v = t
    collist.append(k)
    itemlist.append(v)
    #df[k] = v
 
  df = pd.DataFrame(itemlist,collist)
  #pdb.set_trace()
  #df = pd.DataFrame.from_dict(myObj,index='_id')
  #df = df.drop('_id',axis=1)
  print df.shape
  df = df.T
  print df.shape
  print df.columns
  df.drop('_id', axis=1, inplace=True)
  print df.shape
  X = np.array(df)
  print X.T
  y_pred = 0
  y_pred_proba= model.predict_proba(X)
  #y_pred = model.predict(X)

  html ='<body style="font-family:sans-serif;">'
  html += '<table>'
  html += '<tr>'
  html +='<td>%s</a></td><td align="center" style=\"%s\">%.1f' % (customer_id,loc,float(y_pred_proba[:,1])*100) + '%</td>'
  html += '</tr>'
  html += '</table>'
  html += '</body>'

  return html


'''
Dashboard to check the Quote Status
'''
@app.route('/view')
def view():
  print "Viewing records"
  rec = randint(0,db.test.find().count())
  myObj = db.test.find().limit(-1).skip(rec).next()
  customer_id = str(myObj['customer_ID']) 
  loc = str(myObj['location'])
  print myObj

  return "Customer_ID:" + customer_id + "location:" + loc


if __name__ == '__main__':
  # Bind to PORT if defined, otherwise default to 5000.
  port = int(os.environ.get('PORT', 5000))
  model = pickle.load( open( '../model/predict-purchase', 'rb') )
  app.run(host='0.0.0.0', port=port)