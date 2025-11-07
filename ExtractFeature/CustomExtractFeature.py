import pandas as pd
from ExtractFeature.ExtractFeature import ExtractFeature

class CustomExtractFeature(ExtractFeature):
    def __init__(self):
        super().__init__()

    def getFeatureDataFrame(self, df_txn, df_alert, df_test):
        # 1. 'total_send/recv_amt': total amount sent/received by each acct
        send = df_txn.groupby('from_acct')['txn_amt'].sum().rename('total_send_amt')
        recv = df_txn.groupby('to_acct')['txn_amt'].sum().rename('total_recv_amt')

        # 2. max, min, avg txn_amt for each account
        max_send = df_txn.groupby('from_acct')['txn_amt'].max().rename('max_send_amt')
        min_send = df_txn.groupby('from_acct')['txn_amt'].min().rename('min_send_amt')
        avg_send = df_txn.groupby('from_acct')['txn_amt'].mean().rename('avg_send_amt')
        
        max_recv = df_txn.groupby('to_acct')['txn_amt'].max().rename('max_recv_amt')
        min_recv = df_txn.groupby('to_acct')['txn_amt'].min().rename('min_recv_amt')
        avg_recv = df_txn.groupby('to_acct')['txn_amt'].mean().rename('avg_recv_amt')

        df_result = pd.concat([max_send, min_send, avg_send, max_recv, min_recv, avg_recv, send, recv], axis=1).fillna(0).reset_index()
        df_result.rename(columns={'index': 'acct'}, inplace=True)
        
        # 2. 'is_esun': is esun account or not
        df_from = df_txn[['from_acct', 'from_acct_type']].rename(columns={'from_acct': 'acct', 'from_acct_type': 'is_esun'})
        df_to = df_txn[['to_acct', 'to_acct_type']].rename(columns={'to_acct': 'acct', 'to_acct_type': 'is_esun'})
        df_acc = pd.concat([df_from, df_to], ignore_index=True).drop_duplicates().reset_index(drop=True)
        
        # 4. merge (1), (2), and (3)
        df_result = pd.merge(df_result, df_acc, on='acct', how='left')

        data_X = df_result[(~df_result['acct'].isin(df_test['acct'])) & (df_result['is_esun']==1)].drop(columns=['is_esun']).copy()
        df_y = data_X['acct'].isin(df_alert['acct']).astype(int)
        X_test = df_result[df_result['acct'].isin(df_test['acct'])].drop(columns=['is_esun']).copy()

        print("(Finish) Extract Feature")
        return data_X, df_y, X_test