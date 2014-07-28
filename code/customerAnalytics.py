import pandas as pd
import sys, getopt
import json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pdb
import cPickle as cp 
import pickle
from processData import ProcessData
from modelValidation import ModelValidation
import os
from pymongo import Connection

""" Customer Analytics"""

def customerAnalytics():
	"""
	Description: Purchase prediction based on the quote transactions and scores generated 
	from social media like facebook and twitter. Integrate status of business based on BBB accredition

	"""
	train_data = "../data/train.csv"
	test_data = "../data/test_v2.csv"

	data = ProcessData()
	df_train = data.get_data(train_data)
	df_train = data.clean_data(df_train)
	#pdb.set_trace()
	X,y= data.featurize_data(df_train, db)
	del df_train # memory optimization


	""" Build a Baseline Model """

	print "Running Random Forest Classifier ..."
	clf = RandomForestClassifier(verbose=10, n_estimators=10, n_jobs=-1, max_features=5)
	model = ModelValidation()
	baselineclf = model.get_score(clf,X,y)
	"""
	Area under the ROC curve : 0.794343
	precision of model 0.518552450756
	f score of model 0.270716250149
	recall of model 0.183171521036

	"""

	"""
	Build a pickle for web app to start the purchase prediction

	"""
	cp.dump(clf, open( 'predict-purchase', "wb"))


if __name__ == "__main__":

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
	customerAnalytics()



