import pandas as pd
import numpy as np
import cPickle as cp 
from processData import ProcessData
from graphlab import recommender, SFrame, load_model
import pdb

""" 
Reccommendation engine for upselling the services to the customer
once the quote is created.
"""
class RecommendationEngine(object):
	'''
	A class to create Recommendation Engine.
	'''
	def __init__(self):	
		rec_data = "../data/train.csv"
		data = ProcessData()
		df_rec = data.get_data(rec_data)
		df_rec = data.clean_data(df_rec)
		df_rec = df_rec[df_rec.record_type ==1]
		sf = SFrame(data=df_rec)
		del df_rec # memory optimization

		self.modelA = recommender.create(sf, user_column="customer_ID", item_column="A")
		self.modelB = recommender.create(sf, user_column="customer_ID", item_column="B")
		self.modelC = recommender.create(sf, user_column="customer_ID", item_column="C")
		self.modelD = recommender.create(sf, user_column="customer_ID", item_column="D")
		self.modelE = recommender.create(sf, user_column="customer_ID", item_column="E")
		self.modelF = recommender.create(sf, user_column="customer_ID", item_column="F")


	def get_recommendation(self, id):
		"""
		Description: get recommendations for a given customer id.

		"""

		rec_dict = {}
		resultsA = self.modelA.recommend(users=[id], k=1)
		RA = resultsA.to_dataframe()
		val = int(RA['A'].values)
		if (val >0):
			score = float(RA['score'].values)
			rec_dict['A'] = score
		resultsB = self.modelB.recommend(users=[id], k=1)
		RB = resultsB.to_dataframe()
		val2 = int(RB['B'].values)

		if (val2 >0):
			score = float(RB['score'].values)
			rec_dict['B'] = score

		resultsC = self.modelC.recommend(users=[id], k=1)
		RC = resultsC.to_dataframe()
		val3 = int(RC['C'].values)

		if (val3 >0):
			score = float(RC['score'].values)
			rec_dict['C'] = score


		resultsD = self.modelD.recommend(users=[id], k=1)
		RD = resultsD.to_dataframe()
		val4 = int(RD['D'].values)

		if (val4 >0):
			score = float(RD['score'].values)
			rec_dict['D'] = score

		resultsE = self.modelE.recommend(users=[id], k=1)
		RE = resultsE.to_dataframe()
		val5 = int(RE['E'].values)

		if (val5 >0):
			score = float(RE['score'].values)
			rec_dict['E'] = score

		resultsF = self.modelF.recommend(users=[id], k=1)
		RF = resultsF.to_dataframe()
		val6 = int(RF['F'].values)

		if (val6 >0):
			score = float(RF['score'].values)
			rec_dict['F'] = score

		return rec_dict






