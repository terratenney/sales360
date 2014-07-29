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

""" 
Description: Customer Analytics is the main program to process data, clean data, featurize data.
Run Crossvalidation on the models and compute the scores for further analysis.
"""

def customerAnalytics():
	"""
	Description: Purchase prediction based on the quote transactions and scores generated 
	from social media like facebook and twitter. Since customer sentiment is derived from the number of followers
	from that state. Keeping the scores at level at the moment due to the inability to compute much more detailed metrics.
	"""
	train_data = "../data/train.csv"
	test_data = "../data/test_v2.csv"

	data = ProcessData()
	df_train = data.get_data(train_data)
	df_train = data.clean_data(df_train)

	X,y= data.featurize_data(df_train, db)
	del df_train # memory optimization


	#Build model and run validation

	clf = RandomForestClassifier(verbose=10, n_estimators=10, n_jobs=-1, max_features=5)
	model = ModelValidation()
	baselineclf = model.get_score(clf,X,y)

	"""
	Build a pickle for web app to start the purchase prediction ( compute conversion scores)

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



