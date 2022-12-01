# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : delta_diff.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/18 08:33
"""


import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to correcte the strand')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the delta diff')

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
                    help= 'where to save the filtered file')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output

def filter_delta(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """
    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', low_memory=False)
    mask = df.significant != '-'
    df = df[mask]

    df.to_csv('%s/%s.tsv' % (opts, file.split('_')[0]), sep='\t', index=False)

if __name__ == '__main__':

    # os.chdir('/public/workspace/ryrl/projects/upload/database3/data/diffSites')

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(filter_delta, args=(i,))
    pool.close()
    pool.join()