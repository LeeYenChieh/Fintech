from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class IsSelfFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'from_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]

        df_total = df_valid.groupby('acct').size()
        df_is_self = df_valid[df_valid['is_self_txn'] == "Y"]
        df_feature = df_is_self.groupby('acct').size() / df_total
        df_feature = df_feature.rename('is_self_txn')
        result.append(df_feature)

        print("(Finish) Extract Is Self Transaction Feature")

        return result