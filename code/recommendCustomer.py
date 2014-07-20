import pandas as pd
import json
import numpy as np
import pdb
import cPickle as cp 
import pickle
from processData import ProcessData
from graphlab import recommender, SFrame


""" recommender for Customer """

def recommendCustomer(df, item):
	"""
	Description: Recommend additional services to customer

	"""

	df = df[df.record_type ==1]
	sf = SFrame(data=df)
	del df # memory optimization

	for i in ['A','B','C','D','E','F','G']:
		m = recommender.create(sf, user_column='customer_ID', item_column=i)
	    recs = m.recommend(users=[10000026])
	    print recs

if __name__ == "__main__":
	recommendCustomer()



