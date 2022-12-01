# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : regulatory.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/30 08:12
"""

import argparse
import os

import numpy as np
import pandas as pd
from scipy.stats.mstats import spearmanr
import multiprocessing as mp


parser = argparse.ArgumentParser(description= 'scripts to calculate regulatory genes')

parser.add_argument('--directory_frequency', '-f',
                    dest='dir_freq',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the editing frequency of each dataset')

parser.add_argument('--directory_tpm', '-p',
                    dest='dir_tpm',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the gene tpm expression of each dataset')

parser.add_argument('--samples', '-s',
                    dest='samples',
                    metavar= 'sample_number',
                    type= int,
                    required= True,
                    help= 'The name of the dataset')


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
freq = args.dir_freq
tpm = args.dir_tpm
samples = args.samples
thrd = args.thread
opts = args.output

def freqTpmCorrelation(dirs1:str, dirs2:str, dataset:str, opts:str) -> pd.DataFrame:
    """

    :param opts:
    :param dirs1: directory where stored the expression(TPM)
    :param dirs2: directory where stored the frequency of editing sites
    :param dataset: the name of the dataset
    :return:
    """

    if os.path.exists('%s/%s_tpm.txt' % (dirs1, dataset)) and os.path.exists('%s/%s.tsv' % (dirs2, dataset)):
        tpm = pd.read_csv('%s/%s_tpm.txt' % (dirs1, dataset), sep='\t', header=0, low_memory=False, index_col=0)
        freq = pd.read_csv('%s/%s.tsv' % (dirs2, dataset), sep='\t', header=0, low_memory=False)

        srr = []
        for i in freq.columns:
            if i.__contains__('SRR') and i not in tpm.columns:
                srr.append(i)
        freq = freq.drop(columns=srr)
        freq.Gene_refGene = freq.Gene_refGene.str.split(';')
        freq = freq.explode('Gene_refGene').reset_index(drop=True)
        tpm = pd.merge(freq.iloc[:, 0:5], tpm, how='left', left_on='Gene_refGene', right_index=True)

        array = np.array([])
        for ind, row in freq.iterrows():
            if len(row[5:]) - row[5:].isna().sum() >= samples:
                df1 = pd.DataFrame(freq.iloc[ind, 5:])
                df1 = df1.rename(columns={df1.columns[0]: 'freq'})
                mask = df1.iloc[:, 0].isna()
                df1 = df1.loc[mask == False, ['freq']]

                df2 = pd.DataFrame(tpm.loc[ind, df1.index])
                df2 = df2.rename(columns={df2.columns[0]: 'tpm'})

                array = np.append(array, spearmanr(df1, df2))
                array = np.append(array, len(row[5:]) - row[5:].isna().sum())
            else:
                array = np.append(array, (np.nan, np.nan, len(row[5:]) - row[5:].isna().sum()))
        array = array.reshape(-1, 3)
        df = pd.DataFrame(array, columns=['correlation', 'pvalue', 'samples'])
        df = pd.concat([freq.iloc[:, 0:5], df], axis=1)
        df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)
    else:
        print('%s is not exit' % dataset)
    return

if __name__ == '__main__':

    # dataset = 'GSE103489'
    # tpm = '/public/workspace/ryrl/projects/upload/database3/data/expression/tpm/PA'
    # freq = '/public/workspace/ryrl/projects/upload/database3/data/frequency/allSamples_5'
    #
    # samples = 5
    # thrd = 10
    # opts = '/public/workspace/ryrl/projects/upload/database3/results/RegulationGenes/PA'

    # freqTpmCorrelation(dirs1, dirs2, dataset, opts)

    lst = os.listdir(tpm)
    pool = mp.Pool(thrd)

    for i in lst:
        if not os.path.exists('%s/%s.tsv' % (opts, i.split('_')[0])):
            pool.apply_async(freqTpmCorrelation, args=[tpm, freq, i.split('_')[0], opts])
        else:
            continue
    pool.close()
    pool.join()