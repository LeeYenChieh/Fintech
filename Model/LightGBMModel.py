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
        print("[LightGBM] Start training...")
        trainX = dataset.getTrainX()
        valX = dataset.getValX()
        trainy = dataset.getTrainy()
        valy = dataset.getValy()

        # 建立 LightGBM Dataset
        lgb_train = lgb.Dataset(trainX, label=trainy)
        lgb_val = lgb.Dataset(valX, label=valy, reference=lgb_train)

        # LightGBM 參數
        params = {
        # === 基本設定 ===
        'objective': 'binary',
        'metric': ['binary_logloss', 'auc'],  # 同時計算 AUC
        'boosting_type': 'gbdt',
        'device': 'gpu',               # 啟用 GPU 訓練
        'verbosity': -1,
        'seed': 42,

        # === 學習率與樹深度設定 ===
        'learning_rate': 0.01,         # 小 learning_rate，搭配大量樹數
        'num_leaves': 256,             # 葉節點數增加，學習更細
        'max_depth': -1,               # 不限制深度，由 num_leaves 控制
        'min_data_in_leaf': 20,        # 避免過度擬合（可調小更強）
        'dart_mode': True,    # 或使用 boosting_type='dart'

        # === 抽樣與特徵控制 ===
        'feature_fraction': 0.9,       # 每次訓練使用的特徵比例
        'bagging_fraction': 0.8,       # 每次訓練使用的樣本比例
        'bagging_freq': 1,             # 每棵樹都重新抽樣
        'max_bin': 255,                # 特徵分箱數，GPU 推薦使用 255

        # === 正則化設定 ===
        'lambda_l1': 1.0,              # L1 正則化
        'lambda_l2': 1.0,              # L2 正則化
        'min_gain_to_split': 0.0,      # 分裂所需的最小增益
        'extra_trees': False,          # 關閉 Extremely Randomized Trees 模式

        # === 精度與並行設定 ===
        'n_jobs': -1,                  # CPU 輔助運算核心數
        'gpu_use_dp': False,           # 使用單精度浮點（速度更快）
        }


        # 訓練
        self.model = lgb.train(
            params,
            lgb_train,
            feval=f1_metric,   # 自訂 F1 metric
            valid_sets=[lgb_train, lgb_val],
            valid_names=['train', 'val'],
            callbacks=[lgb.early_stopping(stopping_rounds=1000), lgb.log_evaluation(period=200)],
            num_boost_round=10000,             # 樹數上限，大 learning capacity
        )

        # 儲存模型
        self.model.save_model(self.modelPath)
        print(f"[LightGBM] Model saved to {self.modelPath}")

    def load(self):
        print(f"[LightGBM] Loading model from {self.modelPath} ...")
        if not os.path.exists(self.modelPath):
            raise FileNotFoundError(f"Model file not found: {self.modelPath}")
        self.model = lgb.Booster(model_file=self.modelPath)
        print("[LightGBM] Model loaded successfully.")

    def validate(self, dataset: Dataset, threshold=0.5):
        print("[LightGBM] Start validation...")
        valX = dataset.getValX()
        valy = dataset.getValy()

        preds = self.model.predict(valX, num_iteration=self.model.best_iteration)
        pred_labels = (preds > threshold).astype(int)

        f1 = f1_score(valy, pred_labels)
        print(f"[LightGBM] Validation F1-score: {f1:.4f}")
        return f1

    def test(self, dataset: Dataset, threshold=0.5, testPath=None, dumpPath=None):
        print("[LightGBM] Start testing...")
        testX = dataset.getTestX()
        preds = self.model.predict(testX, num_iteration=self.model.best_iteration)
        pred_labels = (preds > threshold).astype(int)

        # 儲存預測結果
        if testPath is not None and dumpPath is not None:
            os.makedirs(dumpPath, exist_ok=True)
            output_path = os.path.join(dumpPath, "test_predictions.csv")
            result_df = pd.DataFrame({
                "id": range(len(testX)),
                "prediction": pred_labels
            })
            result_df.to_csv(output_path, index=False)
            print(f"[LightGBM] Test results saved to {output_path}")

        print(f"[LightGBM] Test Finished. Total {len(pred_labels)} samples.")
        return pred_labels
