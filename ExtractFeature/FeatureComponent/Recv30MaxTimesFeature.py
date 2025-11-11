from ExtractFeature.FeatureComponent.FeatureDecorator import FeatureDecorator
import pandas as pd

def count_max_within_2days(group):
    count = max_count = 1
    curDay = 1
    prev_diff = None
    for d in group['diff_days'].iloc[1:]:  # 第一筆沒有 diff_days
        curDay += d
        count += 1
        if curDay == 31:
            if count > max_count:
                max_count = count
            curDay = 1
            count = 1
    return max_count

class Recv30MaxTimesFeature(FeatureDecorator):
    def __init__(self, df_txn, df_alert, df_test, component):
        super().__init__(df_txn, df_alert, df_test, component)
    
    def getFeature(self):
        result = super().getFeature()

        df_rename = self.df_txn.rename(columns={'to_acct': 'acct'})
        df_txm_event = df_rename.merge(self.df_alert, on="acct", how="left")
        mask = (df_txm_event['event_date'].isna()) | (df_txm_event['txn_date'] <= df_txm_event['event_date'])
        df_valid = df_txm_event[mask]

        df_valid = df_valid.sort_values(['acct', 'txn_date'])
        df_valid['diff_days'] = df_valid.groupby('acct')['txn_date'].diff()
        df_max = df_valid.groupby('acct').apply(count_max_within_2days)
        df_max = df_max.rename('recv_max_times_30')

        result.append(df_max)
        print("(Finish) Extract Recv Max Times in 30 days Feature")

        return result