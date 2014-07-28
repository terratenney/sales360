"""
Description: Load and clean data from csv files.
"""

from collections import Counter
import pandas as pd
import numpy as np
import pdb

class ProcessData(object):
    '''
    A class to process data.
    '''
    def __init__(self):
        self.df = None  # Build the new dataframe 
        self.features = None
        self.dropfeatures = ['record_type','day','time','state','car_value']
        self.impfeatures = ['shopping_pt','customer_ID','cost','location','age_youngest',
                            'age_oldest','car_age','duration_previous','risk_factor','C_previous','G','group_size']
        self.extrafeatures = [] # build extra feature set to generalize model
        self.label = 'record_type'

    def get_data(self, filename):
        """
        load data into datafrom and return dataframe
        """
        df = pd.read_csv("../data/train.csv")
        self.set_features(df)
        return df


    def clean_data(self,df):
        """
        Clean Data and backfill values to keep the data for better model
        """

    	df = df.fillna(method = 'pad')
 
    	return df

    def set_features(self,df):
        """
        Generate the features from data set
        """

        self.features = df.columns.tolist()
 
        return
    
    def get_features(self,df):
        """
        return list of features from the object
        """

        return self.features 


    def featurize_data(self,df, db):
        """
        Feature Engineering, add costperperson feature
        """

        df['costperperson'] = 1.0 * df.cost/df.group_size
        self.extrafeatures.append('costperperson')

        scores = db.scores
        states = df.state.unique()

        for state in states:
            df.loc[df.state == state,'fscore'] = 0
            df.loc[df.state == state,'tscore'] = 0
            rec = scores.find_one({'state': state},{'fscore': 1, 'tscore' :1})
            if (rec['fscore']) :
                df.loc[df.state == state,'fscore'] = rec['fscore']
            if (rec['tscore']) :
                df.loc[df.state == state,'tscore'] = rec['tscore']
        self.extrafeatures.append('fscore')
        self.extrafeatures.append('tscore')


        train_features = self.impfeatures + self.extrafeatures
        y = df.record_type.values
        X = np.array(df[train_features])
        return X,y

 

