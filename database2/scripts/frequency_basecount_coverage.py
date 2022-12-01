# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/9 11:47
# FileName: frequency_basecount_coverage
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to merge sites by datasets, REVISED')

parser.add_argument('--disease', '-s', dest='disease',
                    metavar='disease', required=True,
                    help='The path to the directory of the disease')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar='path',
                    default='results/QEdit/diff',
                    help='The path to the directory of the diff')

parser.add_argument('--file', '-f', dest='file',
                    metavar='file name',
                    default='de_sites.txt',
                    help='The name of the diff sites')

parser.add_argument('--output', '-o',
                    required=True,
                    dest='output',
                    metavar='path',
                    help='where to save the final file')
args = parser.parse_args()

dis = args.disease
dirs = args.directory
file = args.file
out = args.output


def merge_desite(path, directory='results/QEdit/diff', file='de_sites.txt'):
    lst = []
    cols = ['chromosome', 'position', 'editing_type', 'significant']
    for i in os.listdir(path):
        if i.__contains__('GSE'):
            lst.append(i)

    df = pd.read_csv('%s/%s/%s' % (lst[0], directory, file), sep='\t', header=0)
    if len(df.significant.value_counts()) == 3:
        mask = df.significant == 'yes'
        df = df[mask][cols]

    for i in lst:
        df1 = pd.read_csv('%s/%s/%s' % (i, directory, file), sep='\t', header=0)
        if len(df.significant.value_counts()) == 3:
            mask = df.significant == 'yes'
            df1 = df1[mask][cols]
        df = pd.merge(df, df1,
                      how='outer',
                      on=['chromosome', 'position', 'editing_type', 'significant'])
        df = df.rename(columns={'chromosome': 'Region',
                                'position': 'Position',
                                'editing_type': 'AllSubs'})
    return df


if __name__ == '__main__':

    df = merge_desite(dis, dirs, file)
    if dis.split('/')[-1] == '':
        df.to_csv('%s/%s.txt' % (out, dis.split('/')[-1]))
    else:
        df.to_csv('%s/%s.txt' % (out, dis.split('/')[-2]))
