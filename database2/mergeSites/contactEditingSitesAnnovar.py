# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : contactEditingSitesAnnovar.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/30 13:10
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to contact sites and annovar annotation')

parser.add_argument('--directory1', '-d1',
                    dest='dirs1',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the editing sites')

parser.add_argument('--directory2', '-d2',
                    dest='dirs2',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the annovar annotation')

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
opts = args.output

def contactSitesAnnovar(dirs1:str, dirs2:str, dataset:str) -> pd.DataFrame:
    """

    :param dirs2:
    :param dirs1:
    :param dataset: the name of the dataset
    :return:
    """

    df = pd.read_csv('%s/%s.refGene.rmsk.snp151.txt' % (dirs1, dataset), sep='\t', header=0)
    de = pd.read_csv('%s/%s.tsv' % (dirs2, dataset), sep='\t', header=0)

    df = pd.concat([df.iloc[:, 0:3], de.iloc[:, [5,6,7]], df.iloc[:, 3:]], axis=1)
    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)
    return

if __name__ == '__main__':

    lst = os.listdir(dirs1)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(contactSitesAnnovar, args=(dirs1, dirs2, i.split('.')[0]))
    pool.close()
    pool.join()