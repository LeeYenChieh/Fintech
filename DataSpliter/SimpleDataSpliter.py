from DataSpliter.DataSpliter import DataSpliter
from sklearn.model_selection import train_test_split

class SimpleDataSpliter(DataSpliter):
    def __init__(self):
        super().__init__()

    def splitData(self, X, y):
        X_train_final, X_val, y_train_final, y_val = train_test_split(
            X, y, 
            test_size=0.2,      # 驗證集比例 20%
            stratify=y,   # 根據 y 保持正負樣本比例
            random_state=42
        )

        print("(Finish) Split Data.")
        return X_train_final, X_val, y_train_final, y_val