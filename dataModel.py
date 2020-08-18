import sys
import pandas as pd

class Dataset:

    df = None
    
    # Initialise the Dataframe and 
    def __init__(self,filepath):
        self.df = pd.read_csv(filepath)
        self.df['OFFENCE_MONTH'] = pd.to_datetime(self.df['OFFENCE_MONTH'])


    # Return the Dataframe of records in specified Time Period
    def dateFilter(self,start_date,end_date):
        mask = (self.df['OFFENCE_MONTH'] >= start_date) & (self.df['OFFENCE_MONTH'] < end_date)
        df = self.df.loc[mask]
        return df