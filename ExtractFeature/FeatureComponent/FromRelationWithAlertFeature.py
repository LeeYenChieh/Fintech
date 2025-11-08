from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class FromRelationWithAlertFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'to_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]

        df_from_is_alert = df_valid[df_valid['from_acct'].isin(self.df_test['acct'])]
        df_feature = df_from_is_alert.groupby('acct').size().rename("from_alert")
        result.append(df_feature)

        print("(Finish) Extract From-Relation With Alert Account Feature")

        return result