# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : SitesBiased.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/18 13:37
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to find biased edSites between HC and Patients')

parser.add_argument('--directory1', '-d1',
                    dest='dir1',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the edSites of HC')

parser.add_argument('--directory2', '-d2',
                    dest='dir2',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the edSites of Patient')

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
dir1 = args.dir1
dir2 = args.dir2
thrd = args.thread
opts = args.output

def biasedSites(dataset:str) -> pd.DataFrame:
    """

    :param dataset:
    :return:
    """

    if os.path.exists('%s/%s_HC.tsv' % (dir1, dataset)):
        hc = pd.read_csv('%s/%s_HC.tsv' % (dir1, dataset), sep='\t', header=0, low_memory=False)
        mask = hc['Region'].str.contains(r'(X|Y|M)$')
        hc = hc[mask == False]
        pa = pd.read_csv('%s/%s_Patient.tsv'% (dir2, dataset), sep='\t', header=0, low_memory=False)
        mask = pa['Region'].str.contains(r'(X|Y|M)$')
        pa = pa[mask == False]

        bias_hc = pd.concat([hc, pa, pa]).drop_duplicates(keep=False)
        bias_hc.to_csv('%s/%s/%s.tsv' % (opts, 'HC', dataset), sep='\t', index=False)

        bias_pa = pd.concat([pa, hc, hc]).drop_duplicates(keep=False)
        bias_pa.to_csv('%s/%s/%s.tsv' % (opts, 'PA', dataset), sep='\t', index=False)

        common = pd.merge(hc, pa, on=['Region', 'Position', 'AllSubs'], how='inner')
        common.to_csv('%s/%s/%s.tsv' % (opts, 'Common', dataset), sep='\t', index=False)
    else:
        print('%s have no HC samples' % (dataset,))

    return None

if __name__ == '__main__':

    lst = os.listdir(dir2)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(biasedSites, args=(i.split('_')[0],))
    pool.close()
    pool.join()