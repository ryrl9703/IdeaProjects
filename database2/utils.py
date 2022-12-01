# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : utils.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/19 15:50
"""

import os
import numpy as np
import pandas as pd
from typing import List, Any


def find_file(dirs: str, filename: str) -> list[str]:
    """

    :param filename:
    :param dirs:
    :return:
    """
    lst = []
    for root, dirs, files in os.walk(dirs):
        for i in files:
            if i == filename:
                lst.append('%s/%s' % (root, i))
    return lst


def merge_dataset(path):
    lst = os.listdir(path)
    df = pd.read_csv('%s/%s' % (path, lst[0]), sep='\t', header=0)

    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s' % (path, i), sep='\t', header=0)
        df = pd.merge(df, df1, how='outer',
                      on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'type'])
    return df


def cat_frequency(df: pd.DataFrame):
    """

    :param df: merge_files output, contains all samples Frequency
    :return:
    """
    lst = []
    for i in df.columns:
        if i.startswith('Frequency') and not i.__contains__('None'):
            lst.append(i)

    for i in lst[1:]:
        df['Frequency'] = df['Frequency'].str.cat(df[i], sep=';')

    df = df[['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'type', 'Frequency']]
    df.Frequency = df.Frequency.str.replace('-;', '').str.replace(';-', '')
    return df


def modified_zscore(col: pd.Series) -> pd.Series:
    mid = col.median()
    mid_abs_dev = (np.abs(col - mid)).median()
    mod_zscore: float | Any = 0.6745 * ((col - mid) / mid_abs_dev)
    return mod_zscore


def splitserise(s: pd.Series) -> pd.DataFrame:
    """

    :param s:
    :return:
    """
    df = s.str.split('^', expand=True)[0]
    return df


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


def merge_samples(metaInfo:str, dataset:str, column:str) -> pd.DataFrame:
    """

    :param column:
    :param metaInfo:
    :param dataset:
    :return:
    """
    mask = metaInfo.dataset == dataset
    metaInfo = metaInfo[mask].reset_index(drop=True)

    lst = metaInfo.Run.to_list()
    cols = ['Region', 'Position', 'Reference', 'Strand']
    df = pd.read_csv('%s/%s.tsv' % (lst[0], lst[0]), sep='\t', header=0)[cols]

    for i in lst:
        cols.append(column)
        df1 = pd.read_csv('%s/%s.tsv' % (i, i), sep='\t', header=0)
        df1 = df1.loc[:, cols].rename(columns={column: '%s_%s' % (i, get_disease(metaInfo, i))})
        cols.remove(column)
        df = pd.merge(df, df1, on=cols, how='outer')
    return df


def merge_editingSitesByDataset(dirs:str, sample:list, col:str =None) -> pd.DataFrame:
    """

    :param dirs: the directory where store the all filtered editing sites
    :param sample: the list of the needed samples in a dataset
    :param col: which column you want to keep, default: None
    :return:
    """

    columns = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs']
    df = pd.read_csv('%s/%s/%s.tsv' % (dirs, sample[0], sample[0]), sep='\t', header=0)[columns]

    for i in sample:
        if col is not None:
            columns.append(col)
            df1= pd.read_csv('%s/%s/%s.tsv' % (dirs, i, i), sep='\t', header=0)[columns]
            df = df.rename(columns= {col: i})
            columns.remove(col)
            df = pd.merge(df, df1, how='outer', on=columns)
        else:
            df1 = pd.read_csv('%s/%s/%s.tsv' % (dirs, i, i), sep='\t', header=0)[columns]
            df = pd.merge(df, df1, how='outer', on=columns)
    return df

def select_sample(metaInfo:str, dataset:str, status: str=None) -> list:
    """

    :param dataset: the name of the dataset
    :param metaInfo: the file of the metaInfo contain all samples
    :param status: the status of the sample, default: 'HC'
    :return: the sample list to be used
    """

    if status is not None:
        metaInfo = metaInfo[metaInfo.disease == status]
    samples = metaInfo[metaInfo.dataset == dataset].Run.to_list()

    return samples


def get_sample(metaInfo:pd.DataFrame, dataset:str, status:str) -> list:
    """

    :param dataset: the name of the data set
    :param metaInfo:
    :param status: 'HC'
    :return: sample name list
    """

    mask = metaInfo.Dataset == dataset
    samples = metaInfo[mask]
    if status not in set(samples.Disease):
        print('%s have no %s sample' % (dataset, status))
    else:
        mask = samples.Disease == status
        lst = samples[mask].Run.to_list()

        return lst

# def rm_chrxym_correct_strand(file:str) -> pd.DataFrame:
#     """
#
#     :param file:
#     :return:
#     """
#
#     df = pd.read_csv()