import pandas as pd
from ExtractFeature.ExtractFeature import ExtractFeature
from ExtractFeature.FeatureComponent.BasicComponent import BasicComponent
from ExtractFeature.FeatureComponent.RecvMaxFeature import RecvMaxFeature
from ExtractFeature.FeatureComponent.RecvAverageFeature import RecvAverageFeature
from ExtractFeature.FeatureComponent.SendMaxFeature import SendMaxFeature
from ExtractFeature.FeatureComponent.SendAverageFeature import SendAverageFeature
from ExtractFeature.FeatureComponent.RecvMaxTimesFeature import RecvMaxTimesFeature
from ExtractFeature.FeatureComponent.RecvTimesFeature import RecvTimesFeature
from ExtractFeature.FeatureComponent.SendMaxTimesFeature import SendMaxTimesFeature
from ExtractFeature.FeatureComponent.SendTimesFeature import SendTimesFeature
from ExtractFeature.FeatureComponent.ForeignTxnTimesFeature import ForeignTxnTimesFeature
from ExtractFeature.FeatureComponent.RecvNightTxnTimesFeature import RecvNightTxnTimesFeature
from ExtractFeature.FeatureComponent.SendNightTxnTimesFeature import SendNightTxnTimesFeature
from ExtractFeature.FeatureComponent.IsSelfFeature import IsSelfFeature
from ExtractFeature.FeatureComponent.RecvAlertTimesFeature import RecvAlertTimesFeature
from ExtractFeature.FeatureComponent.RecvAlertSumFeature import RecvAlertSumFeature
from ExtractFeature.FeatureComponent.SendAlertTimesFeature import SendAlertTimesFeature
from ExtractFeature.FeatureComponent.SendAlertSumFeature import SendAlertSumFeature
from ExtractFeature.FeatureComponent.RecvUniqueAcctFeature import RecvUniqueAcctFeature
from ExtractFeature.FeatureComponent.RecvMaxUniqueAcctFeature import RecvMaxUniqueAcctFeature
from ExtractFeature.FeatureComponent.SendUniqueAcctFeature import SendUniqueAcctFeature
from ExtractFeature.FeatureComponent.SendMaxUniqueAcctFeature import SendMaxUniqueAcctFeature
from ExtractFeature.FeatureComponent.SendDiffBankFeature import SendDiffBankFeature
from ExtractFeature.FeatureComponent.RecvDiffBankFeature import RecvDiffBankFeature
from ExtractFeature.FeatureComponent.SendChannelTimesFeature import SendChannelTimesFeature
from ExtractFeature.FeatureComponent.RecvChannelTimesFeature import RecvChannelTimesFeature
from ExtractFeature.FeatureComponent.SendMax5AverageFeature import SendMax5AverageFeature
from ExtractFeature.FeatureComponent.RecvMax5AverageFeature import RecvMax5AverageFeature

class RuleBasedExtractFeature(ExtractFeature):
    def __init__(self):
        super().__init__()

    def getFeatureDataFrame(self, df_txn, df_alert, df_test):
        data_X, data_y, test_X = None, None, None

        feature = BasicComponent()
        feature = RecvMaxFeature(df_txn, df_alert, df_test, feature)
        feature = RecvAverageFeature(df_txn, df_alert, df_test, feature)

        feature = SendMaxFeature(df_txn, df_alert, df_test, feature)
        feature = SendAverageFeature(df_txn, df_alert, df_test, feature)

        feature = RecvMaxTimesFeature(df_txn, df_alert, df_test, feature)
        feature = RecvTimesFeature(df_txn, df_alert, df_test, feature)
        
        feature = SendMaxTimesFeature(df_txn, df_alert, df_test, feature)
        feature = SendTimesFeature(df_txn, df_alert, df_test, feature)

        feature = ForeignTxnTimesFeature(df_txn, df_alert, df_test, feature)

        feature = RecvNightTxnTimesFeature(df_txn, df_alert, df_test, feature)
        feature = SendNightTxnTimesFeature(df_txn, df_alert, df_test, feature)

        feature = IsSelfFeature(df_txn, df_alert, df_test, feature)

        feature = RecvAlertTimesFeature(df_txn, df_alert, df_test, feature)
        feature = RecvAlertSumFeature(df_txn, df_alert, df_test, feature)
        feature = SendAlertTimesFeature(df_txn, df_alert, df_test, feature)
        feature = SendAlertSumFeature(df_txn, df_alert, df_test, feature)

        feature = RecvMaxUniqueAcctFeature(df_txn, df_alert, df_test, feature)
        feature = RecvUniqueAcctFeature(df_txn, df_alert, df_test, feature)

        feature = SendMaxUniqueAcctFeature(df_txn, df_alert, df_test, feature)
        feature = SendUniqueAcctFeature(df_txn, df_alert, df_test, feature)

        feature = SendDiffBankFeature(df_txn, df_alert, df_test, feature)
        feature = RecvDiffBankFeature(df_txn, df_alert, df_test, feature)

        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "1")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "2")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "3")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "4")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "5")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "6")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "7")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "99")
        feature = SendChannelTimesFeature(df_txn, df_alert, df_test, feature, "UNK")

        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "1")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "2")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "3")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "4")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "5")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "6")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "7")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "99")
        feature = RecvChannelTimesFeature(df_txn, df_alert, df_test, feature, "UNK")

        feature = SendMax5AverageFeature(df_txn, df_alert, df_test, feature)
        feature = RecvMax5AverageFeature(df_txn, df_alert, df_test, feature)

        feature_list = feature.getFeature()
        df_result = pd.concat(feature_list, axis=1).fillna(0).reset_index()
        df_result.rename(columns={'index': 'acct'}, inplace=True)

        data_X = df_result[(~df_result['acct'].isin(df_test['acct']))].copy()
        data_y = data_X['acct'].isin(df_alert['acct']).astype(int)
        test_X = df_result[df_result['acct'].isin(df_test['acct'])].copy()

        return data_X, data_y, test_X