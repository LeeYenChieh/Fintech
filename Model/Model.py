from Dataset.Dataset import Dataset

class Model:
    def __init__(self, modelPath):
        self.modelPath = modelPath
    
    def load(self):
        raise NotImplementedError

    def train(self, dataset: Dataset):
        raise NotImplementedError

    def validate(self, dataset: Dataset):
        raise NotImplementedError

    def test(self, dataset: Dataset, dumpPath):
        raise NotImplementedError