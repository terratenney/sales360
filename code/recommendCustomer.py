import pandas as pd
import numpy as np
import cPickle as cp 
from recommendationEngine import RecommendationEngine
import os
from pymongo import Connection
import pdb

"""
Description: Recommendation for Customers about the possible services that they may buy
based on the similar customer profiles from trained data

"""

def recommendCustomer():


	re = RecommendationEngine()

	customers = db.test.find()
	all_customers = set()
	count =0 
	for customer in customers:
		c = customer['customer_ID']
		all_customers.add(c)
		count +=1
		print count

	# clean up recs and reload
	db.recs.remove()

	for cust in all_customers:
		recs = re.get_recommendation(cust)
		recs_sorted = sorted(recs, key=lambda x : recs[x], reverse=True) 

		recommendation1 = "-"
		recommendation2 = "-"
		if (len(recs_sorted) >=2):
			recommendation1 = recs_sorted[0]
			recommendation2 = recs_sorted[1]
		if (len(recs_sorted) ==1):
			recommendation1 = recs_sorted[0]
		cust_rec = {'customer_ID': cust, 'recommendation1' : recommendation1, 'recommendation2': recommendation2}
		db.recs.save(cust_rec)
		print "Processed all recommendations"

	return


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
	recommendCustomer()



