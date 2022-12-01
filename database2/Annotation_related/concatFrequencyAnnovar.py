# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : concatFrequencyAnnovar.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/29 14:56
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to contact Frequency and annovar annotation')

parser.add_argument('--directory1', '-d1',
                    dest='dirs1',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the editing sites and Frequency')

parser.add_argument('--directory2', '-d2',
                    dest='dirs2',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the annovar annotation')

parser.add_argument('--status', '-s',
                    dest='status',
                    metavar= 'status',
                    type= str,
                    choices=['HC', 'PA'],
                    required= True,
                    help= 'The status of sample, choose from ["HC", "PA"]')

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
dirs1 = args.dirs1
dirs2 = args.dirs2
thrd = args.thread
status = args.status
opts = args.output


def concat_Frequency_Annovar(dirs1:str, dirs2:str, dataset:str) -> pd.DataFrame:
    """

    :param dirs1:
    :param dirs2:
    :param dataset:
    :return:
    """

    df = pd.read_csv('%s/%s/%s_%s.tsv' % (dirs1, status, dataset, status), sep='\t', header=0, low_memory=False)
    annovar = pd.read_csv('%s/%s/annovar/%s_%s.tsv' % (dirs2, status, dataset, status), sep='\t', header=0, low_memory=False)
    df = pd.concat([df.iloc[:, 0:4], annovar.iloc[:, [5,6,7]], df.iloc[:, 4:]], axis=1)

    df.to_csv('%s/%s/%s_%s.tsv' % (opts, status, dataset, status), sep='\t', index=None)
    return

if __name__ == '__main__':

    lst = os.listdir('%s/%s' % (dirs1, status))
    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(concat_Frequency_Annovar, args=[dirs1, dirs2, i.split('_')[0]])
    pool.close()
    pool.join()
