# README
## Dump Data CSV
```
python3 main.py --readstrategy raw --rawpathdir {Raw Data Dir} --dump --dumppath ./data --dataspliter custom --feature custom
```

## Different Feature Strategy
1. You should mplement getFeatureDataFrame(self, df_txn, df_alert, df_test) in ExtractFeature/CustomExtractFeature.py
   1. 