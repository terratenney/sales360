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
        self.columns = None
        self.dropColumns = ['record_type','day','time','state','car_value']

    def getData(self, filename):
	    df = pd.read_csv("../data/train.csv")
	    return df

    def fetchFBscore(self,df):
        #df['fb_score'] = 
        return df


    def cleanData(self,df):
        """
        Clean Data and backfill values to keep the data for better model
        """

    	df = df.fillna(method = 'pad')
    	y = df.record_type.values
        self.columns = df.columns
    	df = df.drop(self.dropColumns, axis=1)
        
    	X = np.array(df)
    	return X,y

 


