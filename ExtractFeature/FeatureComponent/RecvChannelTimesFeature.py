from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

class RecvChannelTimesFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component, channel):
        super().__init__(df_txn, df_alert, df_test, component)
        self.channel = channel
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'to_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]
        
        df_valid['channel_type'] = df_valid['channel_type'].astype(str)
        df_channel_txn = df_valid[df_valid['channel_type'] == self.channel]
        df_feature = df_channel_txn.groupby('acct').size()
        df_feature = df_feature.rename(f'recv_channel_{self.channel}_times')
        result.append(df_feature)

        print(f'(Finish) Extract Recv Channel {self.channel} Times Feature')

        return result