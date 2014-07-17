import pandas as pd
import sys, getopt
import json
import numpy as np
import pandas as pd
import json
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import pdb
import cPickle as cp 
import pickle
from processData import ProcessData
from analyzeModel import AnalyzeModel

""" Customer Analytics"""

def customerAnalytics():
	train_data = "../data/train.csv"
	test_data = "../data/test_v2.csv"

	data = ProcessData()
	df_train = data.getData(train_data)
	pdb.set_trace()
	X,y = data.cleanData(df_train)

	# Build a Baseline Model
	print "Running Random Forest Classifier ..."
	clf = RandomForestClassifier(verbose=10, n_estimators=10, n_jobs=-1, max_features=5)
	model = AnalyzeModel()
	model.getScore(clf,X,y)
	"""
	Area under the ROC curve : 0.794343
	precision of model 0.518552450756
	f score of model 0.270716250149
	recall of model 0.183171521036

	"""


if __name__ == "__main__":
	customerAnalytics()



