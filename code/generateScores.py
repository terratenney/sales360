import os
from pymongo import Connection
import random
from processData import ProcessData
import pdb

""" 
Description: Geneate scoring system based on facebook and twitter likes for feature enrichment
Usually facebook and twitter scores at the state level are avaialable for org admin. Assuming that
the scores are available at the state level, continuing with the state level weights and computing scores
for feature engineering. This method can be updated by any org admin to generate scores for their org.
"""

def generate_scores():
	"""
	Description: Build a scoring system based on the customer state.

	"""
	states = ['IN', 'NY', 'PA', 'WV', 'MO', 'OH', 'OK', 'FL', 'OR', 'WA', 'KS',
       'NV', 'ID', 'CO', 'CT', 'AL', 'AR', 'NM', 'MS', 'MD', 'RI', 'UT',
       'ME', 'TN', 'WI', 'MT', 'KY', 'WY', 'NE', 'ND', 'DE', 'GA', 'NH',
       'IA', 'DC', 'SD']
	score_data = "../data/train.csv"
	data = ProcessData()
	df_score = data.getData(score_data)
	df_score = data.cleanData(df_score)

	cust_score = {}
	db.scores.remove()
	for state in states:
		random.seed(9)
		fscore = random.random()
		f_state_weight = fscore * len(df_score[df_score.state == state])/len(df_score)

		random.seed(10)
		tscore = random.random()
		t_state_weight = tscore * len(df_score[df_score.state == state])/len(df_score)
		cust_score = {'state': state, 'fscore' : f_state_weight, 'tscore': t_state_weight }
		db.scores.save(cust_score)

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
	generate_scores()



