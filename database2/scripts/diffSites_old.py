# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/2 10:48
# FileName: diffSites
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to merge sites by datasets, REVISED')

parser.add_argument('--disease', '-s', dest='disease',
                    metavar='disease', required=True,
                    help='The path to the directory of the disease')

parser.add_argument('--file', '-f', dest='file',
                    metavar='file name',
                    default='results/QEdit/diff/de_sites.txt',
                    help='The name of the diff sites')

parser.add_argument('--output', '-o',
                    required=True,
                    dest='output',
                    metavar='path',
                    help='where to save the final file')

args = parser.parse_args()

dis = args.disease
file = args.file
out = args.output


def find_file(dataset: str, target: str = 'de_sites.txt', type: str = 'file'):
    """

    :param dataset:  GEO number of the dataset
    :param target:  the target file or directory name
    :param type:  file or directory
    :return:
    """
    for root, dirs, files in os.walk(dataset):
        if type == 'file':
            if target in files:
                file = os.path.join('%s/%s' % (root, target))
                return file
        else:
            if target in dirs:
                directory = os.path.join('%s/%s' % (root, target))
                return directory
    else:
        print('%s not exit in %s' % (target, dataset))


def cat_significant(df: pd.DataFrame):
    """

    :param df: merge_files output, contains all samples Frequency
    :return:
    """
    lst = []
    for i in df.columns:
        if i.startswith('significant') and not i.__contains__('None'):
            lst.append(i)

    for i in lst[1:]:
        df['significant'] = df['significant'].str.cat(df[i], sep=';')

    df = df[['Region', 'Position', 'AllSubs', 'significant']]
    df.significant = df.significant.str.replace('-;', '').str.replace(';-', '')
    return df


def merge_desites(disease, file='results/QEdit/diff/de_sites.txt'):
    lst = []
    for i in os.listdir(disease):
        if i.__contains__('GSE'):
            lst.append(i)

    cols = ['chromosome', 'position', 'editing_type', 'significant']
    df = pd.read_csv('%s/%s/%s' % (disease, lst[0], file), sep='\t', header=0)[cols]
    mask = df.significant != '-'
    df = df[mask]
    df['dataset'] = lst[0]
    df.significant = df['significant'].str.cat(df.dataset, sep='-')
    df = df.drop(columns=['dataset'])

    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s/%s' % (disease, i, file), sep='\t', header=0)[cols]
        mask = df1.significant != '-'
        df1 = df1[mask]
        df1['dataset'] = i
        df1.significant = df1['significant'].str.cat(df1.dataset, sep='-')
        df1 = df1.drop(columns=['dataset'])

        df = pd.merge(df, df1,
                      how='outer', suffixes=('', '_%s' % i),
                      on=['chromosome', 'position', 'editing_type'])

    df = df.rename(columns={'chromosome': 'Region',
                            'position': 'Position',
                            'editing_type': 'AllSubs'}).fillna('-')

    df = cat_significant(df)
    return df


if __name__ == '__main__':
    df = merge_desites(dis, file)
    if dis.split('/')[-1] == '':
        df.to_csv('%s/%s.txt' % (out, dis.split('/')[-2]), sep='\t', index=None)
    else:
        df.to_csv('%s/%s.txt' % (out, dis.split('/')[-1]), sep='\t', index=None)
