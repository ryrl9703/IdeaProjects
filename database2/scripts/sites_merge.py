# coding: utf-8
# Author: ryrl
# CreateTime: 2022/5/29 11:27
# FileName: sites process
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge sites by datasets')

parser.add_argument('--dataset', '-d', dest='dataset',
                    metavar= 'dataset', required= True,
                    help= 'The dataset that the script to process')

parser.add_argument('--site', '-s',
                    dest='site', metavar='type',
                    required= True, choices= ['redi', 'recoding'],
                    help= 'The site type you want to process, choose from redi and recoding')

parser.add_argument('--metaInfo', '-m',dest='metaInfo',
                    metavar='sample information',required= True,
                    choices= ['metaInfo', 'sample_status'],
                    help= 'The file that contain sample information, choose from metaInfo and sample_status')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dataset = args.dataset
siteType = args.site
metaInfo = args.metaInfo
output = args.output

## TODO add multiprocess if processible

def find_file(dataset:str, target:str, type:str = 'file'):
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


def read_sample(directory:str, sample:str):
    """

    :param directory: where the sites stored
    :param sample: sample name
    :return: the results that filtered
    """
    if os.path.exists('%s/%s/%s' % (directory, sample, sample)):
        df = pd.read_csv('%s/%s/%s' % (directory, sample, sample),sep='\t', header=0)  # 用selectPosition结果一样
        mask = df['AllSubs'].isin(['AG', 'TC'])
        df = df[mask == True]
        mask = df['Coverage-q30'] >= 10
        df = df[mask == True]
        mask = df['Frequency'] >= 0.1
        df = df[mask == True]
        return df
    # elif siteType == 'recoding' and os.path.exists('%s/%s/%s' % (directory, sample, sample)):
    #     df = pd.read_csv('%s/%s/%s' % (directory, sample, sample), sep='\t', header=0)
    #     mask = df['AllSubs'].isin(['AG', 'TC'])
    #     df = df[mask == True]
    #     mask = df['Coverage-q30'] >= 10
    #     df = df[mask == True]
    #     mask = df['Frequency'] >= 0.1
    #     df = df[mask == True]           # 和selectPosition结果一致
    # print('%s/%s/%s not exit' % (directory, sample, sample))
    else:
        print('%s/%s/%s not exit' % (directory, sample, sample))


info = find_file(dataset, '%s.txt' % metaInfo)
dirsites = find_file(dataset, siteType, type='directory')

if metaInfo == 'sample_status':
    file = pd.read_csv(info, sep=',', header=0)
    mask = file.Type != 'HC'

elif metaInfo == 'metaInfo':
    file = pd.read_csv(info, sep='\t', header=0)
    mask = file.disease != 'HC'
else:
    print('metaInfo.txt or sample_status.txt not exit in %s' % dataset)

lst = file.loc[mask == True,  file.columns[0]].to_list()


cols = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Frequency']
df = read_sample(dirsites, lst[0])[cols]
if len(df) == 0:
    df = read_sample(dirsites, lst[1])[cols]

    for i in lst[2:]:
        if os.path.exists('%s/%s' % (dirsites, i)):
            df1 = read_sample(dirsites, i)[cols]
            df = pd.merge(df, df1, how='outer',
                          on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'], suffixes=('', i)).fillna(0)
        else:
            print('%s not exit' % i)
else:

    #  19276
    for i in lst[2:]:
        if os.path.exists('%s/%s' % (dirsites, i)):
            df1 = read_sample(dirsites, i)[cols]
            df = pd.merge(df, df1, how='outer',
                          on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'], suffixes=('', i)).fillna(0)
        else:
            print('%s not exit' % i)

lst = []
for i in df.columns:
    if i.startswith('Frequency'):
        lst.append(i)
df['MeanFrequency'] = df[lst].mean(axis=1)

# 将所有Frequency列合并到一列中
for i in lst[1:]:
    df['Frequency'] = df['Frequency'].astype(str).str.cat(df[i].astype(str), sep=';')
df = df.drop(columns=lst[1:])

if siteType == 'recoding':
    df['siteType'] = siteType

# # 删除多余的Frequency列
# if siteType == 'recoding':
#     df['siteType'] = siteType
#     df = df.drop(columns=df.columns[5:len(df.columns) - 3])
# else:
#     df = df.drop(columns=df.columns[5:len(df.columns) - 2])

df.to_csv('%s/%s_%s.txt' % (output, dataset, siteType), sep='\t', index=None)