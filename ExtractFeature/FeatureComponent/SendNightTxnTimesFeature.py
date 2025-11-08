from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class SendNightTxnTimesFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'from_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]

        df_valid['txn_hour'] = pd.to_datetime(df_valid['txn_time'].astype(str), format='%H:%M:%S').dt.hour
        df_night = df_valid[(df_valid['txn_hour'] >= 0) & (df_valid['txn_hour'] < 6)]
        df_feature = df_night['acct'].value_counts().rename("send_night_txn")
        result.append(df_feature)

        print("(Finish) Extract Send Night Transaction Feature")

        return result