from Dataset.Dataset import Dataset
from Model.Model import Model
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import f1_score

class CatBoostModel(Model):
    def __init__(self):
        self.model = None

    def train(self, dataset: Dataset):
        trainX = dataset.getTrainX()
        valX = dataset.getValX()
        trainy = dataset.getTrainy()
        valy = dataset.getValy()

        # 偵測類別特徵 (CatBoost 可以直接吃 DataFrame)
        cat_features = []
        for col in trainX.columns:
            if trainX[col].dtype == 'object' or col == 'acct':
                cat_features.append(col)

        print(f"Detected categorical features: {cat_features}")

        # 建立訓練與驗證資料池
        train_pool = Pool(trainX, label=trainy, cat_features=cat_features)
        val_pool = Pool(valX, label=valy, cat_features=cat_features)

        # 設定 CatBoost 參數
        self.model = CatBoostClassifier(
            iterations=20000,
            learning_rate=0.02,
            depth=10,
            l2_leaf_reg=5,
            loss_function='Logloss',
            eval_metric='F1',
            auto_class_weights='Balanced',   # 對極端不平衡很有幫助
            early_stopping_rounds=500,
            use_best_model=True,
            random_seed=42,
            verbose=200,
            thread_count=-1,
            task_type="GPU"
        )

        # 開始訓練
        self.model.fit(train_pool, eval_set=val_pool, use_best_model=True)
        self.model.save_model("catboost_model.cbm")

        # 驗證集 F1 分數
        val_pred = self.model.predict(valX)
        f1 = f1_score(valy, val_pred)
        print(f"Validation F1-score: {f1:.4f}")

    def validate(self, dataset: Dataset):
        valX = dataset.getValX()
        valy = dataset.getValy()
        val_pred = self.model.predict(valX)
        f1 = f1_score(valy, val_pred)
        print(f"Validation F1-score: {f1:.4f}")
        return f1

    def test(self, dataset: Dataset, dumpPath):
        testX = dataset.getTestX()
        preds = self.model.predict_proba(testX)[:, 1]  # 取出預測機率
        test_result = testX.copy()
        test_result["pred_prob"] = preds
        test_result.to_csv(dumpPath + "/test_pred.csv", index=False)
        print(f"(Finish) Test prediction saved to {dumpPath}/test_pred.csv")
