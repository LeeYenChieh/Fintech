from Dataset.Dataset import Dataset

class Model:
    def __init__(self):
        pass

    def train(self, dataset: Dataset):
        raise NotImplementedError

    def validate(self, dataset: Dataset):
        raise NotImplementedError

    def test(self, dataset: Dataset, dumpPath):
        raise NotImplementedError