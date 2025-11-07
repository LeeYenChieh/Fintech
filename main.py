from argparse import ArgumentParser

from DataReader.DataReader import DataReader
from DataReader.RawDataReader import RawDataReader
from DataReader.PathDataReader import PathDataReader

from Dataset.Dataset import Dataset

from DataSpliter.DataSpliter import DataSpliter
from DataSpliter.CustomDataSpliter import CustomDataSpliter

from ExtractFeature.ExtractFeature import ExtractFeature
from ExtractFeature.CustomExtractFeature import CustomExtractFeature

from Model.Model import Model
from Model.CustomModel import CustomModel

import os

def parseArgs():
    parser = ArgumentParser()


    parser.add_argument("--readstrategy", choices=["raw", "path"], help="choose read data strategy")

    parser.add_argument("--rawpathdir", help="raw data dir path")
    parser.add_argument("--pathdir", help="feature data dir path")
    parser.add_argument("--dump", action="store_true", help="dump data")
    parser.add_argument("--dumppath", help="store path")

    parser.add_argument("--dataspliter", choices=["custom"], help="choose data splite strategy")
    parser.add_argument("--feature", choices=["custom"], help="choose extract feature strategy")

    parser.add_argument("--train", action="store_true", help="train")
    parser.add_argument("--val", action="store_true", help="val")
    parser.add_argument("--test", action="store_true", help="test")
    parser.add_argument("--resultdumppath", help="dump result path")

    parser.add_argument("--model", choices=["custom"], help="choose model")

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
    
    if args.feature == "custom":
        extractFeature = CustomExtractFeature()

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
    
    if args.train:
        model.train(dataset)
    
    if args.val:
        model.validate(dataset)
    
    if args.test:
        model.test(dataset, args.resultdumppath)

if __name__ == '__main__':
    main()