# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : splitFrequency.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/20 15:48
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d',
                    dest='directory',
                    metavar= 'directory',
                    help= 'The path to the directory contains the samples of the dataset')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    type= int,
                    metavar= 'number_of_process',
                    default= 10,
                    help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.directory
opts = args.output
thrd = args.thread

def split_frequency(path: str, file: str) -> pd.DataFrame:
    """

    :param path: directory stroe the file
    :param file: the target file name
    :return: final splited dataframe contains frequency
    """

    df = pd.read_csv('%s/%s' % (path, file), sep='\t', header=0)
    df = df.rename(columns={'chromosome': 'Region', 'position': 'Position', 'editing_type': 'AllSubs'})
    df1 = df.iloc[:, 3:len(df.columns)-6]

    if len(df.index) > 0:
        df1 = df1.apply(lambda x: x.str.split('^', expand=True)[0], axis=1)
        df = pd.concat([df.iloc[:, 0:3], df1, df.iloc[:, len(df.columns)-5:len(df.columns)-1]], axis=1)

    return df

def run(dataset: str) -> pd.DataFrame:
    """

    :param dataset:
    :return: Null
    """
    df = split_frequency(dirs, dataset)
    df.to_csv('%s/%s.tsv' % (opts, dataset.split('.')[0]), sep='\t', index=None)

if __name__ == '__main__':

    lst = os.listdir()
    for i in lst:
        if not i.startswith('GSE'):
            lst.remove(i)
    mp.Pool(thrd).map(run, lst)