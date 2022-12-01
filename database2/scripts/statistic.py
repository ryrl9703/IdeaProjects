# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : statistic.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/23 15:15
"""
import os

import pandas as pd
import multiprocessing as mp

def statistic(dirs:str, column: str) -> pd.DataFrame:
    """

    :param column:
    :param dirs:
    :return:
    """
    lst = os.listdir(dirs)

    df = pd.read_csv('%s/%s' % (dirs, lst[0]), sep='\t', header=0)
    df.rmsk_tid = df.rmsk_tid.str.split('-', expand=True)[0]
    df = df.loc[:, [column, 'rmsk_tid']]
    df[column] = df[column].str.split(';')
    df = df.explode(column)
    df = df.groupby(column).count()
    df = df.rename(columns={'rmsk_tid': lst[0].split('.')[0]})

    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0)
        df1.rmsk_tid = df1.rmsk_tid.str.split('-', expand=True)[0]
        df1 = df1.loc[:, [column, 'rmsk_tid']]
        df1[column] = df1[column].str.split(';')
        df1 = df1.explode(column)
        df1 = df1.groupby(column).count()
        df1 = df1.rename(columns={'rmsk_tid': i.split('.')[0]})

        df = pd.merge(df, df1, on=[column], how='outer')

    return df

if __name__ == '__main__':
    df = statistic('./contact', 'Gene_refGene')
    df = df.fillna(0)
    df.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database2/'
                         'rediTable/filtered/mergeSitesByDataset/results', 'AluCount.txt'), sep='\t')