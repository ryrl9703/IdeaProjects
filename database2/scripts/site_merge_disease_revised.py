# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/5 17:48
# FileName: site_merge_disease_revised
# Description:


import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to merge sites by datasets, REVISED')

parser.add_argument('--path', '-p', dest='path',
                    metavar='path', required=True,
                    help='The path to the directory contain dataset results')

parser.add_argument('--output', '-o',
                    dest='output', metavar='path',
                    required=True, default='~/projects/upload/database/sites',
                    help='where to save the final file')
args = parser.parse_args()
path = args.path
output = args.output


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


# os.chdir('/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset/SystemicLupusErythematosus')

# lst = os.listdir('./')
#
# df = pd.read_csv('./%s' % lst[0], sep='\t', header=0)
#
# for i in lst[1:]:
#     df1 = pd.read_csv('./%s' % i, sep='\t', header=0)
#     df = pd.merge(df, df1, how='outer', suffixes=('', i.split('.')[0]),
#                   on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'type']).fillna('-')
#
# test = df.drop_duplicates(['Region', 'Position', 'Reference', 'Strand', 'AllSubs'])
#
# test = cat_frequency(df)

if __name__ == '__main__':
    df = merge_dataset(path)
    # df = cat_frequency(df)
    if path.split('/')[-1] == '':
        df.to_csv('%s/%s.txt' % (output, path.split('/')[-2]), sep='\t', index=None)
    else:
        df.to_csv('%s/%s.txt' % (output, path.split('/')[-1]), sep='\t', index=None)
