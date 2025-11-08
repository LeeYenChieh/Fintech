from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class MaxUniqueFromAcctFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'to_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]
        
        df_one_day_nums = df_valid.groupby(['acct', 'txn_date'])['from_acct'].nunique().reset_index()
        df_feature = df_one_day_nums.groupby('acct')['from_acct'].max()
        df_feature = df_feature.rename("max_unique_from")
        result.append(df_feature)

        print("(Finish) Extract Unique From-Account in 24hr Feature")

        return result