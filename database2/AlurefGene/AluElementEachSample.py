# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : AluElementEachSample.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/25 14:48
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

#
# def merge_samples(path:str, sample, columns:list):
#     """
#
#     :param sample: sample
#     :param path: path to the directory contains samples
#     :param columns: column that chosse to use
#     :return:
#     """
#     cols = ['Gene_refGene']
#     df = pd.read_csv('%s/%s.txt' % (path, sample[0]), sep='\t', header=0)
#     df = df[cols]
#
#     cols.extend(columns)
#
#
#
#
# def count_by_gene(path:str, sample:str, column:str) -> pd.DataFrame:
#     """
#
#     :param sample: sample name
#     :param path: path to the directory contains samples
#     :param column: which column you want to count
#     :return:
#     """
#
#     cols = ['Gene_refGene', 'Region', 'Position']
#     df = pd.read_csv('%s/%s.txt' % (path, sample), sep='\t', header=0)
#     return

if __name__ == '__main__':

    os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/annotation/results')
    lst = os.listdir('./contactRediAnnovar')

    print('Count Alu Element'.center(100, '='))
    cols = ['Gene_refGene', 'rmsk_tid']

    df = pd.read_csv('%s/%s' % ('contactRediAnnovar', lst[0]), sep='\t', header=0)
    df = df[cols]
    df.rmsk_tid = df.rmsk_tid.str.split('-', expand=True)[0]
    df = df[df.rmsk_tid == 'Alu']
    df = df.rename(columns={'rmsk_tid': lst[0].split('.')[0]})

    df = df.groupby('Gene_refGene').count()
    # df['Gene_refGene1'] = df.index

    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s' % ('contactRediAnnovar', i), sep='\t', header=0)
        if len(df.index >= 3):
            df1 = df1[cols]
            df1.rmsk_tid = df1.rmsk_tid.str.split('-', expand=True)[0]
            df1 = df1[df1.rmsk_tid == 'Alu']
            df1 = df1.rename(columns={'rmsk_tid': i.split('.')[0]})

            df1 = df1.groupby('Gene_refGene').count()
            # df1 = df1.index

            df = pd.concat([df, df1], axis=1, join='outer')
        else:
            continue

    df = df.fillna(0)

    df.to_csv('%s/%s.txt' % ('contactRediAnnovar', 'df'), sep='\t')


    print('Count Func_refGene'.center(100, '='))
    cols = ['Gene_refGene', 'Func_refGene']

    df = pd.read_csv('%s/%s' % ('contactRediAnnovar', lst[0]), sep='\t', header=0)
    df = df[cols]

    # df.Func_refGene = df.Func_refGene.str.split('-', expand=True)[0]
    # df = df[df.rmsk_tid == 'Alu']
    df = df.rename(columns={'Func_refGene': lst[0].split('.')[0]})

    df = df.groupby('Gene_refGene').count()

    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s' % ('contactRediAnnovar', i), sep='\t', header=0)
        if len(df1.index) >= 3:  # remove SRR6730134 sample
            df1 = df1[cols]
            # df1.Func_refGene = df1.Func_refGene.str.split('-', expand=True)[0]
            # df1 = df1[df1.rmsk_tid == 'Alu']
            df1 = df1.rename(columns={'Func_refGene': i.split('.')[0]})

            df1 = df1.groupby('Gene_refGene').count()
            # df1 = df1.index

            df = pd.concat([df, df1], axis=1, join='outer')
        else:
            continue

    df = df.fillna(0)
    df.to_csv('%s/%s.txt' % ('contactRediAnnovar', 'df_Func_refGene'), sep='\t')