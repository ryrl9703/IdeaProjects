# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : recoding.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/16 02:20
"""

import os
import pandas as pd
import argparse
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to filter recoding sites')

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


def filtered(dirs:str, sample:str, opts:str) -> pd.DataFrame:
    """

    :param opts:
    :param dirs:
    :param sample:
    :return:
    """
    df = pd.read_csv('%s/%s/%s' % (dirs, sample, sample), sep='\t', header=0, low_memory=False)
    mask = df.AllSubs != '-'
    df = df[mask]
    mask = df.Frequency > 0.1
    df = df[mask]
    mask = df['Coverage-q30'] >= 5
    df = df[mask]

    df.to_csv('%s/%s.tsv' % (opts, sample), sep='\t', index=None)
    return


if __name__ == '__main__':

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(filtered, args=[dirs, i, opts])
    pool.close()
    pool.join()
    # os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/recoding')
    #
    #
    # df = pd.read_csv('ori/SRR2443221/SRR2443221', sep='\t', header=0, low_memory=False)
    # mask = df.AllSubs != '-'
    # df = df[mask]
    # mask = df.Frequency > 0.1
    # df = df[mask]
    # mask = df['Coverage-q30'] >= 5
    # df = df[mask]
    # df.to_csv('%s/%s.tsv' % ('filtered', 'test'), sep='\t', index=None)