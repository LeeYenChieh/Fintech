from Dataset.Dataset import Dataset
from Model.Model import Model
import xgboost as xgb
from sklearn.metrics import f1_score
import pandas as pd
import os

def f1_eval(preds, dtrain):
    labels = dtrain.get_label()
    # 二分類預測概率轉標籤
    preds_binary = (preds > 0.5).astype(int)
    return 'f1', f1_score(labels, preds_binary)

class XGBoostModel(Model):
    def __init__(self, modelPath):
        super().__init__(modelPath)
        self.model = None

    def train(self, dataset: Dataset):
        trainX = dataset.getTrainX()
        valX = dataset.getValX()
        trainy = dataset.getTrainy()
        valy = dataset.getValy()

        # 移除不需要的欄位
        trainX_without_acct = trainX
        valX_without_acct = valX

        if 'acct' in trainX.columns:
            trainX_without_acct = trainX.drop('acct', axis=1)
            valX_without_acct = valX.drop('acct', axis=1)

        # 建立 DMatrix
        dtrain = xgb.DMatrix(trainX_without_acct, label=trainy)
        dval = xgb.DMatrix(valX_without_acct, label=valy)

        # XGBoost 參數設定
        params = {
            'objective': 'binary:logistic',
            'eval_metric': 'logloss',
            'tree_method': 'gpu_hist',  # 若無 GPU 可改為 'hist'
            'learning_rate': 0.02,
            'max_depth': 10,
            'lambda': 5,
            'alpha': 0,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'scale_pos_weight': self._compute_pos_weight(trainy),
            'random_state': 42,
        }

        evals = [(dtrain, 'train'), (dval, 'val')]
        self.model = xgb.train(
            params=params,
            dtrain=dtrain,
            num_boost_round=20000,
            evals=evals,
            feval=f1_eval,         # 自訂 F1 metric
            maximize=True,         # F1 越大越好
            early_stopping_rounds=2000,
            verbose_eval=200
        )

        # 儲存模型
        self.model.save_model(self.modelPath)

        # 驗證 F1
        self.validate(dataset)

    def _compute_pos_weight(self, y):
        """
        自動計算不平衡樣本的 scale_pos_weight
        """
        num_pos = sum(y)
        num_neg = len(y) - num_pos
        return num_neg / num_pos if num_pos > 0 else 1

    def load(self):
        self.model = xgb.Booster()
        self.model.load_model(self.modelPath)

    def validate(self, dataset: Dataset, threshold=0.5):
        if self.model is None:
            self.load()

        valX = dataset.getValX()
        valy = dataset.getValy()
        valX_without_acct = valX.drop('acct', axis=1) if 'acct' in valX.columns else valX

        dval = xgb.DMatrix(valX_without_acct)
        preds_prob = self.model.predict(dval, ntree_limit=self.model.best_ntree_limit)
        preds = (preds_prob > threshold).astype(int)

        f1 = f1_score(valy, preds)
        print(f"Validation F1-score: {f1:.4f}")
        return f1

    def test(self, dataset: Dataset, threshold=0.5, testPath="", dumpPath=""):
        if self.model is None:
            self.load()

        testX = dataset.getTestX()
        all_acct = testX["acct"] if 'acct' in testX.columns else pd.Series(range(len(testX)))
        testX_without_acct = testX.drop('acct', axis=1) if 'acct' in testX.columns else testX

        dtest = xgb.DMatrix(testX_without_acct)
        preds_prob = self.model.predict(dtest, ntree_limit=self.model.best_ntree_limit)
        preds = (preds_prob > threshold).astype(int)
        preds = pd.Series(preds, name="label")
        preds = pd.concat([all_acct, preds], axis=1)

        originTest = pd.read_csv(testPath)
        originTest.drop('label', axis=1, inplace=True)
        result = pd.merge(originTest, preds, how="left", on="acct").fillna(0)
        result = result[['acct', 'label']]

        result.to_csv(dumpPath, index=False)
        print(f"(Finish) Test prediction saved to {dumpPath}")
