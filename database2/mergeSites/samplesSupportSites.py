# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : samplesSupportSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/15 16:25
"""


import os
import pandas as pd
import argparse
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to calculate the number of sample support editing sites')

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



def calculate_samples(dirs:str, dataset:str, opts:str) -> pd.DataFrame:
    """

    :param opts:
    :param dataset:
    :type dirs: object
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, dataset), sep='\t', header=0, low_memory=False)
    df = pd.concat([df.iloc[:, 0:3],
                    len(df.iloc[:, 3:].columns) - df.iloc[:, 3:].isnull().sum(axis=1),
                    df.iloc[:, 3:]], axis=1)
    df = df.rename(columns={df.columns[3]: 'SamplesSupport'})
    # mask = df.samplesSupport >= 5
    # df = df[mask == True]

    df.to_csv('%s/%s.tsv' % (opts, dataset.split('.')[0]), sep='\t', index=None)
    return

if __name__ == '__main__':

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(calculate_samples, args=[dirs, i, opts])
    pool.close()
    pool.join()
    # os.chdir('/public/workspace/ryrl/projects/upload/database2/'
    #          'rediTable/filtered/mergeSitesByDataset/sites_frequency/frequency')
    #
    # lst = os.listdir('./')
    # df = pd.read_csv(lst[0], sep='\t', header=0)
    # df = pd.concat([df.iloc[:, 0:3],
    #                 len(df.iloc[:, 3:].columns) - df.iloc[:, 3:].isnull().sum(axis=1),
    #                 df.iloc[:, 3:]], axis=1)
    # df = df.rename(columns={df.columns[3]: 'samplesSupport'})
