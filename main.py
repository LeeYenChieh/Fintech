from argparse import ArgumentParser

from DataReader.DataReader import DataReader
from DataReader.RawDataReader import RawDataReader
from DataReader.PathDataReader import PathDataReader

from Dataset.Dataset import Dataset

from DataSpliter.DataSpliter import DataSpliter
from DataSpliter.SimpleDataSpliter import SimpleDataSpliter
from DataSpliter.SMOKEDataSpliter import SMOKEDataSpliter
from DataSpliter.CustomDataSpliter import CustomDataSpliter

from ExtractFeature.ExtractFeature import ExtractFeature
from ExtractFeature.SimpleExtractFeature import SimpleExtractFeature
from ExtractFeature.RuleBasedExtractFeature import RuleBasedExtractFeature
from ExtractFeature.CustomExtractFeature import CustomExtractFeature

from Model.Model import Model
from Model.CatBoostModel import CatBoostModel
from Model.LightGBMModel import LightGBM
from Model.XGBoost import XGBoostModel
from Model.CustomModel import CustomModel

import os

def parseArgs():
    parser = ArgumentParser()


    parser.add_argument("--readstrategy", choices=["raw", "path"], help="choose read data strategy")

    parser.add_argument("--rawpathdir", help="raw data dir path")
    parser.add_argument("--pathdir", help="feature data dir path")
    parser.add_argument("--dump", action="store_true", help="dump data")
    parser.add_argument("--dumppath", help="store path")

    parser.add_argument("--dataspliter", choices=["simple", "custom", "smoke"], help="choose data splite strategy")
    parser.add_argument("--feature", choices=["simple", "custom", "rule"], help="choose extract feature strategy")

    parser.add_argument("--train", action="store_true", help="train")
    parser.add_argument("--val", action="store_true", help="val")
    parser.add_argument("--test", action="store_true", help="test")
    parser.add_argument("--testpath", help="test path")
    parser.add_argument("--resultdumppath", help="dump result path")
    parser.add_argument("--threshold", type=float, help="dump result path")

    parser.add_argument("--model", choices=["custom", "cat", "lightgbm","xgb"], help="choose model")
    parser.add_argument("--modelpath", help="store model path")

    args = parser.parse_args()
    return args

def main():
    args = parseArgs()

    dataset: Dataset = None
    datareader: DataReader = None
    extractFeature: ExtractFeature = None
    dataSpliter: DataSpliter = None

    if args.dataspliter == "custom":
        dataSpliter = CustomDataSpliter()
    elif args.dataspliter == "simple":
        dataSpliter = SimpleDataSpliter()
    elif args.dataspliter == "smoke":
        dataSpliter = SMOKEDataSpliter()
    
    if args.feature == "custom":
        extractFeature = CustomExtractFeature()
    elif args.feature == "simple":
        extractFeature = SimpleExtractFeature()
    elif args.feature == "rule":
        extractFeature = RuleBasedExtractFeature()

    if args.readstrategy == "raw":
        datareader = RawDataReader(args.rawpathdir)
        datareader.setDataSpliter(dataSpliter)
        datareader.setExtractFeature(extractFeature)
    elif args.readstrategy == "path":
        datareader = PathDataReader(args.pathdir)
    else:
        raise NotImplementedError
    
    dataset = datareader.getCSVDataset()
    if args.dump:
        os.makedirs(args.dumppath, exist_ok=True)
        dataset.dump(args.dumppath)
    dataset.logInfo()

    model: Model = None
    if args.model == "custom":
        model = CustomModel()
    elif args.model == "cat":
        model = CatBoostModel(args.modelpath)
    elif args.model == "lightgbm":
        model = LightGBM(args.modelpath)
    elif args.model == "xgb":
        model = XGBoostModel(args.modelpath)
    
    if args.train:
        model.train(dataset)
    
    if args.val:
        model.validate(dataset, args.threshold)
    
    if args.test:
        model.test(dataset, args.threshold, args.testpath, args.resultdumppath)

if __name__ == '__main__':
    main()