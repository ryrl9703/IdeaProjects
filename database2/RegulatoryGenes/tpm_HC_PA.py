# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : tpm_HC_PA.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/29 18:37
"""


import argparse
import os

import pandas as pd
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to get the tpm of the patients')


parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the gene tpm expression of each dataset')

parser.add_argument('--metaInfo', '-m',
                    dest='metaInfo',
                    metavar= 'metaInfo',
                    type= str,
                    required= True,
                    help= 'The full path of the metaInfo file')


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
meta = args.metaInfo
thrd = args.thread
opts = args.output


def getTpm(dataset:str, meta:str) -> pd.DataFrame:
    """

    :param meta: the full path of hte metaInfo file
    :param dataset: name of the dataset
    :return:
    """

    tpm = pd.read_csv('%s/%s_tpm.txt' % (dirs, dataset), sep='\t', header=0, low_memory=False)

    metaInfo = pd.read_csv(meta, sep='\t', header=0, low_memory=False)
    mask = metaInfo.Dataset == dataset
    metaInfo = metaInfo[mask]
    mask = metaInfo.Disease != 'HC'
    run = list(metaInfo[mask].Run)

    srr = []
    for i in tpm.columns:
        if i not in run[:]:
            srr.append(i)
        else:
            continue
    tpm = tpm.drop(columns=srr)
    tpm.to_csv('%s/%s_tpm.txt' % (opts, dataset), sep='\t', index=True)

    return




if __name__ == '__main__':

    # Test:
    # dirs = '/public/workspace/ryrl/projects/upload/database3/data/expression/tpm/SRR'
    # meta = '/public/workspace/ryrl/projects/upload/database3/data/metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt'
    # thrd = 10
    # opts = '/public/workspace/ryrl/projects/upload/database3/data/expression/tpm/PA'


    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(getTpm, args=[i.split('_')[0], meta])
    pool.close()
    pool.join()