from DataSpliter.DataSpliter import DataSpliter
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

class SMOKEDataSpliter(DataSpliter):
    def __init__(self):
        super().__init__()

    def splitData(self, X, y):

        X_train, X_val, y_train, y_val = train_test_split(
            X, y, 
            test_size=0.2,      # 驗證集比例 20%
            stratify=y_train,   # 根據 y 保持正負樣本比例
            random_state=42
        )

        smote = SMOTE(random_state=42, sampling_strategy='auto', k_neighbors=5)

        X_no_acct = X_train.drop(columns=['acct'])
        X_resampled, y_resampled = smote.fit_resample(X_no_acct, y_train)
        X_resampled["acct"] = "None"

        print("(Finish) Split Data.")
        return X_resampled, X_val, y_resampled, y_val