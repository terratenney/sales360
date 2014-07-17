"""
Description: Load and clean data from csv files.
"""

from collections import Counter
import pandas as pd
import numpy as np

class ProcessData(object):
    '''
    A class to process data.
    '''
    def __init__(self):
        self.df = None  # Build the new dataframe 

    def getData(self, filename):
	    df = pd.read_csv("../data/train.csv")
	    return df

    def fetchFBscore(self,df):
        #df['fb_score'] = 
        return df


    def cleanData(self,df):

    	#df = df.fillna(df.mean())
        df = df.dropna()
    	y = df.record_type.values
    	df = df.drop(['record_type','day','time','state','car_value'], axis=1)
    	X = np.array(df)
    	return X,y

 


