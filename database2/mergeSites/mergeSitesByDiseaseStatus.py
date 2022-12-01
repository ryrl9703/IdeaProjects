# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesByDiseaseStatus.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/20 10:20
"""

import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merg edSites by Disease')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the datatset')

parser.add_argument('--ststus', '-s',
                    dest='status',
                    metavar= 'status',
                    choices=['HC', 'Patient'],
                    type= str,
                    required=True,
                    help= 'The status of the sample, choose from "HC" and "Patient"')

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
status = args.status


def mergeSites(metaInfo:pd.DataFrame, disease:str, dirs:str) -> pd.DataFrame:
    """

    :param dirs:
    :param disease:
    :param metaInfo:
    :return:
    """

    mask = metaInfo.Disease_id == disease
    lst = list(set(metaInfo[mask].Dataset))

    df = pd.read_csv('%s/%s_%s.tsv' % (dirs, lst[0], status), sep='\t', header=0, low_memory=False)

    for i in lst[1:]:
        de = pd.read_csv('%s/%s_%s.tsv' % (dirs, i, status), sep='\t', header=0, low_memory=False)
        df = pd.merge(df, de, how='outer', on=['Region', 'Position', 'Strand', 'AllSubs'])

    df.to_csv('%s/%s.tsv' % (opts, disease), sep='\t', index=None)
    return None

if __name__ == '__main__':

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                           'data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)

    dis = list(set(metaInfo.Disease_id))

    pool = mp.Pool(thrd)
    for i in dis:
        pool.apply_async(mergeSites, args=[metaInfo, i, dirs])
    pool.close()
    pool.join()
