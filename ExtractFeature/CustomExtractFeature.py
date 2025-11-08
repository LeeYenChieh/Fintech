import pandas as pd
from ExtractFeature.ExtractFeature import ExtractFeature

class CustomExtractFeature(ExtractFeature):
    def __init__(self):
        super().__init__()

    def getFeatureDataFrame(self, df_txn, df_alert, df_test):
        data_X, data_y, test_X = None, None, None
        # implement your feature extraction method

        return data_X, data_y, test_X