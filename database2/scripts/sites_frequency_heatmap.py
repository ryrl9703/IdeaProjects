# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : sites_frequency_heatmap.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/28 08:55
"""

import os
from typing import List

import numpy as np
import pandas as pd
import argparse

# parser = argparse.ArgumentParser(description='scripts to Statistics')
#
# parser.add_argument('--directory', '-d', dest='directory',
#                     metavar='directory', required=True,
#                     help='The path to the directory contain results')
#
# parser.add_argument('--output', '-o',
#                     dest='output', metavar='path',
#                     required=True, default='~/projects/upload/database/sites',
#                     help='where to save the final file')
# args = parser.parse_args()
# dirs = args.directory
# output = args.output

os.chdir('/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset')


def getfrequency(file: str) -> pd.DataFrame:
    """

    :param file: path to the file
    :return: data frame
    """
    df = pd.read_csv(file, sep='\t', header=0, low_memory=False)
    cols = []
    for i in df.columns:
        if i.__contains__('Frequency'):
            cols.append(i)
    df = pd.concat([df.iloc[:, 0:9], df[cols]], axis=1)
    return df


def filepath(path: str, pattern: str = None) -> list:
    """

    :param pattern:
    :param path:
    :return:
    """
    lst: list[str] = []
    for root, dirs, files in os.walk(path):
        for i in files:
            if pattern is not None:
                if i.__contains__(pattern):
                    lst.append('%s/%s' % (root, i))
            else:
                lst.append('%s/%s' % (root, i))
    return lst


if __name__ == '__main__':
    for i in filepath('./', 'contanct'):
        df = getfrequency(i)
        df.to_csv('%s/%s_%s' % ('/public/workspace/ryrl/projects/upload/database2/finalResults/frequencyByDataSets/ori',
                                i.split('/')[-2], i.split('/')[-1]), sep='\t', index=None)

    # Mean
    for i in filepath('/public/workspace/ryrl/projects/upload/'
                      'database2/finalResults/frequencyByDataSets/ori'):
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = df.iloc[:, 8:].fillna(0).groupby(by='genes').mean()
        df.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database2/'
                             'finalResults/frequencyByDataSets/gene_editing_frequency/mean',
                             i.split('/')[-1]), sep='\t')

    lst = filepath('/public/workspace/ryrl/projects/upload/database2/'
                   'finalResults/frequencyByDataSets/gene_editing_frequency/mean')

    df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
    for i in lst[1:]:
        df1 = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = pd.merge(df, df1, on=['genes'], how='outer')

    df = df.fillna(0)

    df.to_csv('%s/gene_mean_frequency.txt' %
              '/public/workspace/ryrl/projects/upload/database2/finalResults/frequencyByDataSets',
              sep='\t', index=None)

    # split sites
    for i in filepath('/public/workspace/ryrl/projects/upload/database2/finalResults/frequencyByDataSets/ori'):
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False).iloc[:, 0:5]
        df.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database2/'
                             'finalResults/frequencyByDataSets/sites', i.split('/')[-1]), sep='\t', index=None)

    # Median
    for i in filepath('/public/workspace/ryrl/projects/upload/'
                      'database2/finalResults/frequencyByDataSets/ori'):
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = df.iloc[:, 8:].fillna(0).groupby(by='genes').median()
        df.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database2/'
                             'finalResults/frequencyByDataSets/gene_editing_frequency/median',
                             i.split('/')[-1]), sep='\t')

    # merge
    lst = filepath('/public/workspace/ryrl/projects/upload/database2/'
                   'finalResults/frequencyByDataSets/gene_editing_frequency/median')

    df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
    for i in lst[1:]:
        df1 = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = pd.merge(df, df1, on=['genes'], how='outer')

    df = df.fillna(0)

    df.to_csv('%s/gene_median_frequency.txt' %
              '/public/workspace/ryrl/projects/upload/database2/'
              'finalResults/frequencyByDataSets/gene_editing_frequency', sep='\t', index=None)

    # rediportal annotate and annovar annotate merge
    os.chdir('/public/workspace/ryrl/projects/upload/database2/finalResults/frequencyByDataSets/')
    for i in filepath('./ori'):
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df1 = pd.read_csv('%s/%s' % ('annotation', i.split('/')[-1]), sep='\t', header=0, low_memory=False)
        df = pd.concat([df.iloc[:, 0:9], df1.iloc[:, 5:]], axis=1)
        df.to_csv('%s/%s' % ('./contact', i.split('/')[-1]), sep='\t', index=None)

    # df['0'].value_counts()
    df = pd.read_csv(filepath('./contact')[0], sep='\t', header=0, low_memory=False)
    df1 = pd.DataFrame(df['0'].value_counts())
    df1 = df1.rename(columns={df1.columns[0]: filepath('./contact')[0].split('/')[-1]})
    for i in filepath('./contact')[1:]:
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        s = pd.DataFrame(df['0'].value_counts())
        s = s.rename(columns={s.columns[0]: i.split('/')[-1]})
        df1 = pd.merge(df1, s, left_index=True, right_index=True, how='outer')
    df1 = df1.fillna(0)
    df1.to_csv('%s/%s' % ('Statistics', 'region.txt'), sep='\t', index=True)

    redi = pd.read_csv('/public/workspace/ryrl/reference/rediportal/TABLE1_hg38.txt',
                       sep='\t', header=0, low_memory=False)

    for i in filepath('./contact'):
        df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = df.drop(columns=['type_y'])
        df.columns = df.columns.str.replace('_x', '')
        df.to_csv('./contact/%s' % i.split('/')[-1], sep='\t', index=None)

        df.iloc[:, 14].value_counts()

    df = pd.read_csv('./gene_editing_frequency/gene_mean_frequency.txt', sep='\t', header=0)
    (df.iloc[:, 1:] == 0).astype(int).sum(axis=1).max()

    os.chdir('/public/workspace/ryrl/projects/upload/database2/finalResults/editingSites/results')
    lst = os.listdir('../ori')
    df = pd.read_csv('../ori/%s' % lst[0], sep='\t', header=0, low_memory=False)