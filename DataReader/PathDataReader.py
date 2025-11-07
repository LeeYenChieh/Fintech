from DataReader.DataReader import DataReader
from Dataset.CSVDataset import CSVDataset
import pandas as pd
import os

class PathDataReader(DataReader):
    
    def __init__(self, dataDir: str):
        super().__init__()
        self.dataDir = dataDir

    def getCSVDataset(self) -> CSVDataset:
        train = pd.read_csv(os.path.join(self.dataDir, 'train.csv'))
        val = pd.read_csv(os.path.join(self.dataDir, 'validation.csv'))
        test = pd.read_csv(os.path.join(self.dataDir, 'test.csv'))
        return CSVDataset(train.drop("label", axis=1), val.drop("label", axis=1), train["label"], val["label"], test)