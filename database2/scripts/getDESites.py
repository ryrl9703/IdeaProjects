# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : getDESites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/18 12:52
"""

import os
import argparse
import numpy as np
import pandas as pd
import scipy.stats as ss
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d',
                    dest='directory',
                    metavar= 'directory',
                    help= 'The path to the directory contains the samples of the dataset')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    type= int,
                    metavar= 'number_of_process',
                    default= 10,
                    help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.directory
opts = args.output
thrd = args.thread

def get_disease(metaInfo: pd.DataFrame, sample: str) -> str:
    """

    :param metaInfo:
    :param sample:
    :return:
    """
    for ind, srr in enumerate(metaInfo.Run):
        if srr == sample:
            return metaInfo.disease[ind]

def get_columns(df: pd.DataFrame, disease: str) -> list:
    """

    :param disease:
    :param df:
    :return:
    """
    lst = []
    lst1 = []
    for i in df.columns:
        if i.__contains__(disease):
            lst.append(i)
        elif i.startswith('SRR'):
            lst1.append(i)
    return lst,lst1

def merge_samples(metaInfo: str, dataset: str,) -> pd.DataFrame:
    """

    :param metaInfo:
    :param dataset:
    :return:
    """
    mask = metaInfo.dataset == dataset
    metaInfo = metaInfo[mask].reset_index(drop=True)

    lst = metaInfo.Run.to_list()
    cols = ['Region', 'Position', 'Reference', 'Strand']
    df = pd.read_csv('%s/%s.tsv' % (lst[0], lst[0]), sep='\t', header=0)
    # df = df.loc[:, cols].rename(columns={'Frequency': '%s_%s' % (lst[0], get_disease(metaInfo, lst[0]))})

    for i in lst:
        cols.append('Frequency')
        df1 = pd.read_csv('%s/%s.tsv' % (i, i), sep='\t', header=0)
        df1 = df1.loc[:, cols].rename(columns={'Frequency': '%s_%s' % (i, get_disease(metaInfo, i))})
        cols.remove('Frequency')
        df = pd.merge(df, df1, on=cols, how='outer')
    return df

def get_pval(df: pd.DataFrame):
    """

    :param df:
    :return:
    """

    control_sample, disease_sample = get_columns(df, 'HC')

    arr = np.array([])
    for i in df.index:
        ctrl_freq = df.loc[i, control_sample].dropna().astype(float)
        dise_freq = df.loc[i, disease_sample].dropna().astype(float)

        if len(ctrl_freq) >= 3 and len(dise_freq) >= 3:
            s, p = ss.mannwhitneyu(ctrl_freq, dise_freq, alternative='two-sided')
            arr = np.append(arr, p)
        else:
            arr = np.append(arr, np.nan)
    return pd.DataFrame(arr)

def run(dataset:str):
    """

    :param dataset:
    :return:
    """

    df = merge_samples(metaInfo, dataset)

    p = get_pval(df)
    df = pd.concat([df, p], axis=1)

    df = df.rename(columns={df.columns[len(df.columns)]: 'pvalue'})
    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)


if __name__ == '__main__':
    # os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/ori')
    os.chdir(dirs)
    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)

    dataset = metaInfo.dataset.drop_duplicates().reset_index(drop=True).to_list()
    mp.Pool(thrd).map(run, dataset)
    # metaInfo[metaInfo.dataset == 'GSE171770'].disease.value_counts()  # GSE158952

    # dataset.remove('GSE158952')
    # dataset.remove('GSE171770')
    # dataset.remove('GSE72509')
    # mp.Pool(int(thrd)).map(run, dataset)
    #
    # df = merge_samples(metaInfo, 'GSE121212')
    #
    # p = get_pval(df)
    # df = pd.concat([df, p], axis=1)
    #
    # df = df.rename(columns={df.columns[120]: 'pvalue'})
    # df.to_csv('../test/diffSites/GSE121212.txt', sep='\t', index=None)


    # (df.pvalue < 0.05).value_counts()
    # (df[df.columns[120]] < 0.05).vqalue_counts()
    # q = mp.Queue()
    # p = mp.Process(target=get_pval, args=(df,))
    # p.start()
    # p.join()
    # mp.Pool(10).map(get_pval, df)