from DataReader.DataReader import DataReader
from ExtractFeature.ExtractFeature import ExtractFeature
from DataSpliter.DataSpliter import DataSpliter
from Dataset.CSVDataset import CSVDataset
import pandas as pd
import os

class RawDataReader(DataReader):
    
    def __init__(self, rawDataDir: str):
        super().__init__()
        self.rawDataDir = rawDataDir
        self.df_txn, self.df_alert, self.df_test = self.loadCSV()
        self.extractFeature: ExtractFeature = None
        self.dataSpliter: DataSpliter = None
    
    def setExtractFeature(self, e: ExtractFeature):
        self.extractFeature = e

    def setDataSpliter(self, s: DataSpliter):
        self.dataSpliter = s

    def getCSVDataset(self) -> CSVDataset:
        X, y, testX = self.extractFeature.getFeatureDataFrame(self.df_txn, self.df_alert, self.df_test)
        trainX, valX, trainy, valy = self.dataSpliter.splitData(X, y)
        return CSVDataset(trainX, valX, trainy, valy, testX)

    def loadCSV(self):
        df_txn = pd.read_csv(os.path.join(self.rawDataDir, 'acct_transaction.csv'))
        df_alert = pd.read_csv(os.path.join(self.rawDataDir, 'acct_alert.csv'))
        df_test = pd.read_csv(os.path.join(self.rawDataDir, 'acct_predict.csv'))
    
        print("(Finish) Load Dataset.")
        return df_txn, df_alert, df_test