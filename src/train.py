#!/usr/bin/env python3
import logging
import re
import typing as tp

import datasets
import transformers


logging.basicConfig(filename='logs.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def get_dataset() -> datasets.DatasetDict:

    def basic_text_preprocess(dataset_example):
        dataset_example['text'] = re.sub('\s+', ' ', dataset_example['text']).strip()
        return dataset_example


    def is_unique(element: tp.Dict[str, tp.Any], column_name: str, memory_set: tp.Set) -> bool:
        if element[column_name] in memory_set:
            return False
        memory_set.add(element[column_name])
        return True


    dataset = datasets.load_dataset('takiholadi/kill-me-please-dataset')
    dataset = dataset.remove_columns(['tags', 'votes', 'url', 'datetime'])
    dataset = dataset.map(basic_text_preprocess, desc='Dataset basic preprocessing')

    already_seen = set()
    n_of_rows_before = sum(dataset.num_rows.values())
    dataset = dataset.filter(  # drop duplicates by certain column
        function=lambda x: is_unique(element=x, column_name='text', memory_set=already_seen),
        num_proc=None,  # important proceed in single process
        load_from_cache_file=False,  # otherwise sometimes get wrong
        desc='Daatset filtering for duplicates',
    )
    logger.info(f'Number of rows, before and after deduplication: {n_of_rows_before} -> {sum(dataset.num_rows.values())}')
    logger.info(f'Dataset len: {sum(dataset.num_rows.values())}')

    return dataset


if __name__ == '__main__':
    logger.info('-=-=-=-=-=- START -=-=-=-=-=-')
    transformers.set_seed(567)
    dataset = get_dataset()
    logger.info('-=-=-=-=-=- END -=-=-=-=-=-')

