# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : ADAR.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/5 00:42
"""

import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats.mstats import spearmanr
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to extract expression(TPM)')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the tpm of each dataset')


parser.add_argument('--gene', '-g',
                    dest='gene',
                    metavar= 'gene',
                    nargs= '+',
                    type= str,
                    default=['ADAR', 'ADARB1', 'ADARB2', 'ADARB2-AS1'],
                    help= 'The genes you want to extract from dataset, defalut: [ADAR,ADARB1,ADARB2,ADARB2-AS1]')


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
gene = args.gene
thrd = args.thread
opts = args.output


def get_tpm(dirs:str, file:str, gene:list) -> pd.DataFrame:
    """

    :param dirs: the directory that contain the expression of each dataset
    :param file: the file name of the expression
    :param gene:
    :return: None
    """


    tpm = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=0)
    for i in gene[:]:
        if i not in tpm.index:
            gene.remove(i)
    # while not set(gene).issubset(set(tpm.index)):  # 空集合是任意集合的子集
    #     gene.pop()
    else:
        if len(gene) > 0:
            tpm = tpm.T[gene]
            tpm.to_csv('%s/%s_ADAR_tpm.txt' % (opts, file.split('_')[0]), sep='\t', index=True)
        else:
            print('%s is not contain genes you want' % file)
    return

if __name__ == '__main__':

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(get_tpm, args=[dirs, i, gene])
    pool.close()
    pool.join()