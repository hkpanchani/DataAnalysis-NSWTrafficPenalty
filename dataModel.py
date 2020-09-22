import sys
import pandas as pd
from PyQt5.QtCore import QAbstractTableModel, Qt

class Dataset:

    df = None
    
    # Initialise the Dataframe and 
    def __init__(self,filepath):
        self.df = pd.read_csv(filepath,low_memory=False)
        self.df['OFFENCE_MONTH'] = pd.to_datetime(self.df['OFFENCE_MONTH'])

    def getModel(self,dataframe):
        model = pandasModel(dataframe)
        return model

    # Returns Model of AN Entire CSV
    def getAllData(self):
        return pandasModel(self.ds)

    # Return the Dataframe of records in specified Time Period
    def dateFilter(self,start_date,end_date):
        mask = (self.df['OFFENCE_MONTH'] >= start_date) & (self.df['OFFENCE_MONTH'] < end_date)
        df = self.df.loc[mask]
        return self.getModel(df)


class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None