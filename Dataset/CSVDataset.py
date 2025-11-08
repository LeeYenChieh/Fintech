from Dataset.Dataset import Dataset
import pandas as pd

class CSVDataset(Dataset):
    def __init__(self, trainX, valX, trainy, valy, testX):
        super().__init__()
        self.trainX = trainX
        self.valX = valX
        self.trainy = trainy
        self.valy = valy
        self.testX = testX
    
    def getTrainX(self):
        return self.trainX

    def getValX(self):
        return self.valX
    
    def getTrainy(self):
        return self.trainy
    
    def getValy(self):
        return self.valy
    
    def getTestX(self):
        return self.testX
    
    def dump(self, dirPath):
        train = pd.concat([self.trainX, self.trainy.to_frame(name="label")], axis=1)
        val = pd.concat([self.valX, self.valy.to_frame(name="label")], axis=1)
        print(val[val['label'] == 1].head(40))

        train.to_csv(dirPath + '/train.csv', index=False, encoding='utf-8')
        val.to_csv(dirPath + '/validation.csv', index=False, encoding='utf-8')
        self.testX.to_csv(dirPath + '/test.csv', index=False, encoding='utf-8')

        print("(Finish) Data Dump.")

    def logInfo(self):
        print("=" * 30)
        print("Train Dataset")
        print(f'Data Nums: {len(self.trainX)}')
        print(f'Alert Account Data Nums: {self.trainy.sum()}')
        print("=" * 30)
        print("Validation Dataset")
        print(f'Data Nums: {len(self.valX)}')
        print(f'Alert Account Data Nums: {self.valy.sum()}')
        print("=" * 30)
        print("Test Dataset")
        print(f'Data Nums: {len(self.testX)}')
        print("=" * 30)