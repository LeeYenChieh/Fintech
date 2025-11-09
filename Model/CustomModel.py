from Dataset.Dataset import Dataset
from Model.Model import Model

class CustomModel(Model):
    def __init__(self):
        pass

    def train(self, dataset: Dataset):
        print("train")
    
    def load(self):
        pass

    def validate(self, dataset: Dataset):
        print("validation")

    def test(self, dataset: Dataset, testPath, dumpPath):
        print("test")