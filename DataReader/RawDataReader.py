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

        num_unique_values = df_txn["currency_type"].unique()

        exchange_rate_to_TWD = {
            'TWD': 1,
            'USD': 30,      # 1 USD = 30 TWD
            'JPY': 0.25,    # 1 JPY = 0.25 TWD
            'AUD': 20,      # 1 AUD = 20 TWD
            'CNY': 4.2,     # 1 CNY = 4.2 TWD
            'EUR': 32,      # 1 EUR = 32 TWD
            'SEK': 3,       # 1 SEK = 3 TWD
            'GBP': 37,      # 1 GBP = 37 TWD
            'HKD': 3.8,     # 1 HKD = 3.8 TWD
            'THB': 0.88,    # 1 THB = 0.88 TWD
            'CAD': 23,      # 1 CAD = 23 TWD
            'NZD': 18,      # 1 NZD = 18 TWD
            'CHF': 33,      # 1 CHF = 33 TWD
            'SGD': 22,      # 1 SGD = 22 TWD
            'ZAR': 1.6,     # 1 ZAR = 1.6 TWD
            'MXN': 1.5      # 1 MXN = 1.5 TWD
        }
        df_txn['txn_amt'] = df_txn['txn_amt'] * df_txn['currency_type'].map(exchange_rate_to_TWD)
    
        print("(Finish) Load Dataset.")
        return df_txn, df_alert, df_test