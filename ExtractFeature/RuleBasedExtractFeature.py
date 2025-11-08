import pandas as pd
from ExtractFeature.ExtractFeature import ExtractFeature
from ExtractFeature.FeatureComponent.BasicComponent import BasicComponent
from ExtractFeature.FeatureComponent.MaxRecvFeature import MaxRecvFeature
from ExtractFeature.FeatureComponent.AverageRecvFeature import AverageRecvFeature
from ExtractFeature.FeatureComponent.MaxSendFeature import MaxSendFeature
from ExtractFeature.FeatureComponent.AverageSendFeature import AverageSendFeature
from ExtractFeature.FeatureComponent.MaxRecvTimesFeature import MaxRecvTimesFeature
from ExtractFeature.FeatureComponent.RecvTimesFeature import RecvTimesFeature
from ExtractFeature.FeatureComponent.MaxSendTimesFeature import MaxSendTimesFeature
from ExtractFeature.FeatureComponent.SendTimesFeature import SendTimesFeature
from ExtractFeature.FeatureComponent.ForeignTxnTimesFeature import ForeignTxnTimesFeature
from ExtractFeature.FeatureComponent.RecvNightTxnTimesFeature import RecvNightTxnTimesFeature
from ExtractFeature.FeatureComponent.SendNightTxnTimesFeature import SendNightTxnTimesFeature
from ExtractFeature.FeatureComponent.IsSelfFeature import IsSelfFeature
from ExtractFeature.FeatureComponent.FromRelationWithAlertFeature import FromRelationWithAlertFeature
from ExtractFeature.FeatureComponent.ToRelationWithAlertFeature import ToRelationWithAlertFeature
from ExtractFeature.FeatureComponent.UniqueFromAcctFeature import UniqueFromAcctFeature
from ExtractFeature.FeatureComponent.MaxUniqueFromAcctFeature import MaxUniqueFromAcctFeature
from ExtractFeature.FeatureComponent.UniqueToAcctFeature import UniqueToAcctFeature
from ExtractFeature.FeatureComponent.MaxUniqueToAcctFeature import MaxUniqueToAcctFeature
from ExtractFeature.FeatureComponent.SendDiffBankFeature import SendDiffBankFeature
from ExtractFeature.FeatureComponent.RecvDiffBankFeature import RecvDiffBankFeature

class RuleBasedExtractFeature(ExtractFeature):
    def __init__(self):
        super().__init__()

    def getFeatureDataFrame(self, df_txn, df_alert, df_test):
        data_X, data_y, test_X = None, None, None

        feature = BasicComponent()
        feature = MaxRecvFeature(df_txn, df_alert, df_test, feature)
        feature = AverageRecvFeature(df_txn, df_alert, df_test, feature)

        feature = MaxSendFeature(df_txn, df_alert, df_test, feature)
        feature = AverageSendFeature(df_txn, df_alert, df_test, feature)

        feature = MaxRecvTimesFeature(df_txn, df_alert, df_test, feature)
        feature = RecvTimesFeature(df_txn, df_alert, df_test, feature)
        
        feature = MaxSendTimesFeature(df_txn, df_alert, df_test, feature)
        feature = SendTimesFeature(df_txn, df_alert, df_test, feature)

        feature = ForeignTxnTimesFeature(df_txn, df_alert, df_test, feature)

        feature = RecvNightTxnTimesFeature(df_txn, df_alert, df_test, feature)
        feature = SendNightTxnTimesFeature(df_txn, df_alert, df_test, feature)

        feature = IsSelfFeature(df_txn, df_alert, df_test, feature)

        feature = FromRelationWithAlertFeature(df_txn, df_alert, df_test, feature)
        feature = ToRelationWithAlertFeature(df_txn, df_alert, df_test, feature)

        feature = MaxUniqueFromAcctFeature(df_txn, df_alert, df_test, feature)
        feature = UniqueFromAcctFeature(df_txn, df_alert, df_test, feature)

        feature = MaxUniqueToAcctFeature(df_txn, df_alert, df_test, feature)
        feature = UniqueToAcctFeature(df_txn, df_alert, df_test, feature)

        feature = SendDiffBankFeature(df_txn, df_alert, df_test, feature)
        feature = RecvDiffBankFeature(df_txn, df_alert, df_test, feature)

        feature_list = feature.getFeature()
        df_result = pd.concat(feature_list, axis=1).fillna(0).reset_index()
        df_result.rename(columns={'index': 'acct'}, inplace=True)

        data_X = df_result[(~df_result['acct'].isin(df_test['acct']))].copy()
        data_y = data_X['acct'].isin(df_alert['acct']).astype(int)
        test_X = df_result[df_result['acct'].isin(df_test['acct'])].copy()

        return data_X, data_y, test_X