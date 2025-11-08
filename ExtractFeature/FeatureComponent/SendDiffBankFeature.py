from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class SendDiffBankFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'from_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]
        
        df_diff_txn = df_valid[(df_valid['from_acct_type'] != 1) | (df_valid['to_acct_type'] != 1)]
        df_feature = df_diff_txn.groupby('acct').size() / df_valid.groupby('acct').size()
        df_feature = df_feature.rename('send_diff_bank')
        result.append(df_feature)

        print("(Finish) Extract Send Different Bank Feature")

        return result