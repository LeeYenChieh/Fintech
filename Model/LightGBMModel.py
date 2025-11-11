from Dataset.Dataset import Dataset
from Model.Model import Model
import lightgbm as lgb
from sklearn.metrics import f1_score
import os
import pandas as pd

def f1_metric(y_pred, dataset):
    """
    LightGBM 自定義 metric function
    - y_pred: 模型預測值（機率）
    - dataset: lgb.Dataset 對象
    """
    y_true = dataset.get_label()
    # 將機率轉換為二分類，閾值可自己調整
    y_pred_labels = (y_pred > 0.5).astype(int)
    f1 = f1_score(y_true, y_pred_labels)
    return 'f1', f1, True  # True 表示越大越好

class LightGBM(Model):
    def __init__(self, modelPath=None):
        super().__init__(modelPath)
        self.model = None
        self.modelPath = modelPath

    def train(self, dataset: Dataset):
        trainX = dataset.getTrainX()
        valX = dataset.getValX()
        trainy = dataset.getTrainy()
        valy = dataset.getValy()

        trainX_without_acct = trainX
        valX_without_acct = valX

        if 'acct' in trainX.columns.tolist():
            trainX_without_acct = trainX.drop('acct', axis = 1)
            valX_without_acct = valX.drop('acct', axis = 1)

        # 建立 LightGBM Dataset
        lgb_train = lgb.Dataset(trainX_without_acct, label=trainy)
        lgb_val = lgb.Dataset(valX_without_acct, label=valy, reference=lgb_train)

        # LightGBM 參數
        params = {
            # === 基本設定 ===
            'objective': 'binary',
            'metric': ['binary_logloss', 'auc'],  # 同時計算 AUC
            'boosting_type': 'gbdt',
            # 'device': 'gpu',               # 啟用 GPU 訓練
            # 'gpu_device_id': -1,
            'num_thread': 70,
            'verbosity': 2,
            'seed': 42,

            # === 學習率與樹深度設定 ===
            'learning_rate': 0.05,         # 小 learning_rate，搭配大量樹數
            'num_leaves': 64,             # 葉節點數增加，學習更細
            'max_depth': -1,               # 不限制深度，由 num_leaves 控制
            'min_data_in_leaf': 20,        # 避免過度擬合（可調小更強）

            # === 抽樣與特徵控制 ===
            'feature_fraction': 0.7,       # 每次訓練使用的特徵比例
            'bagging_fraction': 0.7,       # 每次訓練使用的樣本比例
            'bagging_freq': 5,             # 每棵樹都重新抽樣
            'max_bin': 63,
            # 'gpu_use_dp': True,

            # === 正則化設定 ===
            'lambda_l1': 1.0,              # L1 正則化
            'lambda_l2': 1.0,              # L2 正則化
            'min_gain_to_split': 0.0,      # 分裂所需的最小增益
            'extra_trees': False,          # 關閉 Extremely Randomized Trees 模式
        }

        # 訓練
        self.model = lgb.train(
            params=params,
            train_set=lgb_train,
            feval=f1_metric,   # 自訂 F1 metric
            valid_sets=[lgb_train, lgb_val],
            valid_names=['train', 'val'],
            callbacks=[lgb.log_evaluation(period=10), lgb.early_stopping(stopping_rounds=50)],
            num_boost_round=1000,             # 樹數上限，大 learning capacity
        )

        # 儲存模型
        self.model.save_model(self.modelPath)
        self.validate()

    def load(self):
        print(f"[LightGBM] Loading model from {self.modelPath} ...")
        self.model = lgb.Booster(model_file=self.modelPath)

    def validate(self, dataset: Dataset, threshold=0.5):
        if self.model == None:
            self.load()
        valX = dataset.getValX()
        valy = dataset.getValy()
        
        valX_without_acct = valX

        if 'acct' in valX.columns.tolist():
            valX_without_acct = valX.drop('acct', axis = 1)

        preds = self.model.predict(valX_without_acct, num_iteration=self.model.best_iteration)
        pred_labels = (preds > threshold).astype(int)

        f1 = f1_score(valy, pred_labels)
        print(f"[LightGBM] Validation F1-score: {f1:.4f}")
        return f1

    def test(self, dataset: Dataset, threshold=0.5, testPath=None, dumpPath=None):
        if self.model == None:
            self.load()
        testX = dataset.getTestX()
        testX_without_acct = testX
        all_acct = testX["acct"]

        if 'acct' in testX.columns.tolist():
            testX_without_acct = testX.drop('acct', axis = 1)

        preds = self.model.predict(testX_without_acct, num_iteration=self.model.best_iteration)
        pred_labels = (preds > threshold).astype(int)

        pred_labels = pd.Series(pred_labels).rename("label")
        pred_labels = pd.concat([all_acct, pred_labels], axis=1)

        originTest = pd.read_csv(testPath)
        originTest.drop('label', axis=1, inplace=True)
        
        result = pd.merge(originTest, pred_labels, how="left", on="acct").fillna(0)
        result = result[['acct', 'label']]
        result.to_csv(dumpPath, index=False)
        print(f"(Finish) Test prediction saved to {dumpPath}")
        return pred_labels
