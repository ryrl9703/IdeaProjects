# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeRecodingSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/15 16:13
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp
import sys
sys.path.append('/public/workspace/ryrl/idea/database2')
from utils import get_sample

parser = argparse.ArgumentParser(description= 'scripts to correcte p value of the correlation')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the original recoding sites')

parser.add_argument('--status', '-s',
                    dest='status',
                    metavar= 'sample status',
                    type= str,
                    required=True,
                    choices=['HC', 'Patient'],
                    help= 'The status of the sample')


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
parser.add_argument('--output2', '-o2',
                    dest= 'output2',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the filtered recoding sites')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output
status = args.status
opts2 = args.output2


def merge_by_dataset(dirs:str, metaInfo:pd.DataFrame, dataset:str) -> pd.DataFrame:
    """

    :param dirs:
    :param metaInfo:
    :param dataset:
    :return:
    """

    lst = get_sample(metaInfo, dataset, status)

    for i in lst[:]:
        if not os.path.exists('%s/%s' % (dirs, i)):
            lst.remove(i)

    df = pd.read_csv('%s/%s/%s' % (dirs, lst[0],lst[0]), sep='\t', header=0, low_memory=False)  # .iloc[:, [0,1,7,3]]
    mask = df.AllSubs != '-'
    df = df[mask]
    mask = df['Coverage-q30'] >= 5
    df = df[mask]
    mask = df.Frequency >= 0.1
    df = df[mask].reset_index(drop=True)
    df.to_csv('%s/%s.tsv' % (opts2, lst[0]), sep='\t', index=None)

    for i in lst[1:]:

        df1 = pd.read_csv('%s/%s/%s' % (dirs, i, i), sep='\t', header=0, low_memory=False)  # .iloc[:, [0,1,7,3]]
        mask = df1.AllSubs != '-'
        df1 = df1[mask]
        mask = df1['Coverage-q30'] >= 5
        df1 = df1[mask]
        mask = df1.Frequency >= 0.1
        df1 = df1[mask].reset_index(drop=True)
        df1.to_csv('%s/%s.tsv' % (opts2, i), sep='\t', index=None)
        # if df1.shape[0] > 0:
        de = pd.merge(df.iloc[:, [0,1,7,3]], df1.iloc[:, [0,1,7,3]], on=['Region', 'Position', 'AllSubs', 'Strand'], how='outer')
        de.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)
    return None

if __name__ == '__main__':


    # dirs = '/public/workspace/ryrl/projects/upload/database3/data/recoding_ori'
    # dataset = 'GSE89408'
    # status = 'HC'

    metaInfo = pd.read_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database3/data/metaInfo',
                                      'metaInfo_IFNscore_HallMarkscores_1023.txt'), sep='\t', header=0, low_memory=False)
    mask = metaInfo.Disease != 'HC'
    metaInfo.iloc[metaInfo[mask].Disease.index, 3] = 'Patient'

    pool = mp.Pool(thrd)

    for i in list(set(metaInfo.Dataset)):
        pool.apply_async(merge_by_dataset, args=[dirs, metaInfo, i])
    pool.close()
    pool.join()