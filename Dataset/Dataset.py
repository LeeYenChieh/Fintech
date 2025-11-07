class Dataset:
    def __init__(self):
        pass

    def getTrainX(self):
        raise NotImplementedError

    def getValX(self):
        raise NotImplementedError
    
    def getTrainy(self):
        raise NotImplementedError
    
    def getValy(self):
        raise NotImplementedError
    
    def getTestX(self):
        raise NotImplementedError
    
    def dump(self, dirPath):
        raise NotImplementedError