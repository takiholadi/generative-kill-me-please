#!/usr/bin/env python3
import argparse
import json
import logging
import pathlib
import typing as tp

import numpy as np
import pandas as pd
import sklearn
import sklearn.preprocessing
import skmultilearn
import skmultilearn.model_selection


logging.basicConfig(filename='logs.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def process(input_jsons_dirpath: str, output_csvs_dirpath: str, test_size: float = 0.1) -> tp.Tuple[str, str]:
    dicts = []
    for each_filepath in pathlib.Path(input_jsons_dirpath).glob('*.json'):
        with open(each_filepath) as f:
            each_dict = json.load(f)
        dicts.append(each_dict)
    df = pd.DataFrame(dicts)

    df['temp_for_sort'] = df['url'].apply(lambda x: int(pathlib.Path(x).stem))
    df = df.sort_values(by='temp_for_sort')
    wanted_columns = ['text', 'tags', 'votes', 'url', 'datetime']
    df = df[wanted_columns]

    mlb = sklearn.preprocessing.MultiLabelBinarizer()
    y = mlb.fit_transform(df['tags'].apply(lambda x: x.split(', ')))
    np.random.seed(567)
    X_train, _, X_test, _ = skmultilearn.model_selection.iterative_train_test_split(df.values, y, test_size=test_size)
    train_df = pd.DataFrame(data=X_train, columns=df.columns)
    test_df = pd.DataFrame(data=X_test, columns=df.columns)
    assert test_df[test_df['tags'] == ''].empty  # train contains 1 sample with tags=''

    train_filepath = str((pathlib.Path(output_csvs_dirpath) / 'train.csv').resolve())
    test_filepath = str((pathlib.Path(output_csvs_dirpath) / 'test.csv').resolve())
    assert not pathlib.Path(train_filepath).exists()
    assert not pathlib.Path(test_filepath).exists()
    pathlib.Path(train_filepath).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(test_filepath).parent.mkdir(parents=True, exist_ok=True)
    train_df.to_csv(train_filepath, index=False)
    test_df.to_csv(test_filepath, index=False)

    return (train_filepath, test_filepath)


if __name__ == '__main__':
    logger.info('-=-=-=-=-=- START -=-=-=-=-=-')
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_jsons_dirpath', type=str)
    parser.add_argument('--output_csvs_dirpath', type=str)
    args = parser.parse_args()
    (train_filepath, test_filepath) = process(input_jsons_dirpath=args.input_jsons_dirpath, output_csvs_dirpath=args.output_csvs_dirpath)
    logger.info(f'Train filepath: {train_filepath}')
    logger.info(f'Test filepath: {test_filepath}')
    logger.info('-=-=-=-=-=- END -=-=-=-=-=-')
