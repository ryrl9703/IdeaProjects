# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesByDataSet.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/30 09:25
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to calculate regulatory genes')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the datasets')


parser.add_argument('--thread', '-t',
                    dest='thread',
                    metavar= 'number_of_process',
                    default= 10,
                    type= int,
                    help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output


def mergeSites(dirs:str, dataset:str) -> pd.DataFrame:
    """

    :param dirs: the directory contains the datset
    :param dataset: the name of the dataset
    :return: None
    """

    lst = os.listdir('%s/%s' % (dirs, dataset))
    cols = ['Region', 'Position', 'AllSubs']
    df = pd.read_csv('%s/%s/%s/%s.tsv' % (dirs, dataset, lst[0], lst[0]), sep='\t', header=0)[cols]

    for i in lst:
        cols.append('Frequency')
        df1 = pd.read_csv('%s/%s/%s/%s.tsv' % (dirs, dataset, i, i), sep='\t', header=0)[cols]
        df1 = df1.rename(columns={'Frequency': i})
        cols.remove('Frequency')
        df = pd.merge(df, df1, on=cols, how='outer')

    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)
    return

if __name__ == '__main__':

    lst = os.listdir(dirs)
    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(mergeSites, args=[dirs, i])
    pool.close()
    pool.join()
