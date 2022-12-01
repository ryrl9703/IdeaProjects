# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : pvalue_correction.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/14 11:16
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp
import statsmodels.stats.multitest as sm

parser = argparse.ArgumentParser(description= 'scripts to correcte p value of the correlation')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the Regulatory sites results')

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


def fdr(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """
    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=0, low_memory=False).dropna(axis=0)
    df = pd.concat([df, pd.DataFrame(sm.fdrcorrection( pvals=df.pvalue,alpha=0.1)).T], axis=1)
    df = df.rename(columns={df.columns[8]: 'significant', df.columns[9]: 'fdr'})
    mask = df.significant == True
    df = df[mask]
    mask = abs(df.correlation) >= 0.4
    df = df[mask]

    if df.shape[0] > 0:
        df.to_csv('%s/%s' % (opts, file), sep='\t', index=None)
    else:
        print('%s no regulatory sites find' % file)

    return None

def main():

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(fdr, args=(i,))

    pool.close()
    pool.join()




if __name__ == '__main__':

    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/RegulationGenes/PA/ori'
    # thrd = 30
    # opts = '/public/workspace/ryrl/projects/upload/database3/results/RegulationGenes/PA/FDR'
    # lst = os.listdir(dirs)
    # for i in lst:
    #     fdr(i)

    main()
