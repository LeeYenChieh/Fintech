from Dataset.Dataset import Dataset
from Model.Model import Model
from catboost import CatBoostClassifier, Pool
from sklearn.metrics import f1_score
import pandas as pd

class CatBoostModel(Model):
    def __init__(self, modelPath):
        super().__init__(modelPath)
        self.model = None

    def train(self, dataset: Dataset):
        trainX = dataset.getTrainX()
        valX = dataset.getValX()
        trainy = dataset.getTrainy()
        valy = dataset.getValy()

        trainX_without_acct = trainX
        valX_without_acct = valX

        # 偵測類別特徵 (CatBoost 可以直接吃 DataFrame)
        cat_features = []
        print(trainX.columns.tolist())
        if 'acct' in trainX.columns.tolist():
            trainX_without_acct = trainX.drop('acct', axis = 1)
            valX_without_acct = valX.drop('acct', axis = 1)

        print(f"Detected categorical features: {cat_features}")

        # 建立訓練與驗證資料池
        train_pool = Pool(trainX_without_acct, label=trainy, cat_features=cat_features)
        val_pool = Pool(valX_without_acct, label=valy, cat_features=cat_features)

        # 設定 CatBoost 參數
        self.model = CatBoostClassifier(
            iterations=20000,
            learning_rate=0.02,
            depth=10,
            l2_leaf_reg=5,
            loss_function='Logloss',
            eval_metric='F1',
            auto_class_weights='Balanced',   # 對極端不平衡很有幫助
            early_stopping_rounds=2000,
            use_best_model=True,
            random_seed=42,
            verbose=200,
            thread_count=-1,
            task_type="GPU"
        )

        # 開始訓練
        self.model.fit(train_pool, eval_set=val_pool, use_best_model=True)
        self.model.save_model(self.modelPath)

        # 驗證集 F1 分數
        self.validate(dataset)

    def load(self):
        self.model = CatBoostClassifier()
        self.model.load_model(self.modelPath)

    def validate(self, dataset: Dataset, threshold=0.5):
        if self.model == None:
            self.load()
        valX = dataset.getValX()
        valy = dataset.getValy()

        valX_without_acct = valX

        if 'acct' in valX.columns.tolist():
            valX_without_acct = valX.drop('acct', axis = 1)
        
        val_pred = pd.Series((self.model.predict_proba(valX_without_acct)[:,1] > threshold).astype(int))
        
        f1 = f1_score(valy, val_pred)
        print(f"Validation F1-score: {f1:.4f}")
        return f1

    def test(self, dataset: Dataset, threshold=0.5, testPath="", dumpPath=""):
        if self.model == None:
            self.load()
        testX = dataset.getTestX()

        testX_without_acct = testX
        all_acct = testX["acct"]

        if 'acct' in testX.columns.tolist():
            testX_without_acct = testX.drop('acct', axis = 1)

        preds = (self.model.predict_proba(testX_without_acct)[:,1] > threshold).astype(int)
        preds = pd.Series(preds).rename("label")
        preds = pd.concat([all_acct, preds], axis=1)

        originTest = pd.read_csv(testPath)
        originTest.drop('label', axis=1, inplace=True)
        
        result = pd.merge(originTest, preds, how="left", on="acct").fillna(0)
        result = result[['acct', 'label']]
        result.to_csv(dumpPath, index=False)
        print(f"(Finish) Test prediction saved to {dumpPath}")
