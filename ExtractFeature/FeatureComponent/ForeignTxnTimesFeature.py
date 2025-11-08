from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class ForeignTxnTimesFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'from_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]

        foreign_txn = df_valid[df_valid['currency_type'] != 'TWD']
        acct_foreign_count = foreign_txn['acct'].value_counts().rename("foreign_txn")
        result.append(acct_foreign_count)

        print("(Finish) Extract Foreign Transaction Times Feature")

        return result