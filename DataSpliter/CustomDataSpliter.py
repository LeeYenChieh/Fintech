from DataSpliter.DataSpliter import DataSpliter
from sklearn.model_selection import train_test_split

class CustomDataSpliter(DataSpliter):
    def __init__(self):
        super().__init__()

    def splitData(self, X, y):
        X_train_final, X_val, y_train_final, y_val = None, None, None, None
        # Implement your data spliter method

        return X_train_final, X_val, y_train_final, y_val