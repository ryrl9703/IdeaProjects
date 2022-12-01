# coding: utf-8
# Author: ryrl
# CreateTime: 2022/5/29 11:27
# FileName: sites process
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge sites by datasets')

parser.add_argument('--dataset', '-d',
                    dest='dataset', metavar= 'dataset', required= True,
                    help= 'The dataset that the script to process')

parser.add_argument('--site', '-s',
                    dest='site', metavar='sites type',
                    required= True, choices= ['redi', 'recoding'],
                    help= 'The site type you want to process')

parser.add_argument('--metaInfo', '-m',
                    dest='metaInfo', metavar='sample information',
                    required= True, choices= ['metaInfo', 'sample_status'],
                    help= 'The file that contain sample information')
parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')

args = parser.parse_args()
dataset = args.dataset
siteType = args.type
metaInfo = args.metaInfo
output = args.output


def find_file(dataset:str, target:str, type:str = 'file'):
    """

    :param dataset:
    :param target:
    :param type:
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


def filter_sites(directory:str, sample:str):
    """

    :param directory: where the sites stored
    :param sample:
    :return: the results that filtered
    """
    df = pd.read_csv('%s/%s/%s' % (directory, sample, sample),sep='\t', header=0).\
        drop(columns=['gCoverage-q30', 'gMeanQ','gBaseCount[A,C,G,T]', 'gAllSubs', 'gFrequency'])
    mask = df['AllSubs'].isin(['AG', 'TC'])
    df = df[mask == True]
    mask = df['Coverage-q30'] >= 10
    df = df[mask == True]
    return df






info = find_file(dataset, '%s.txt' % metaInfo)
sites = find_file(dataset, siteType, type='directory')

if metaInfo == 'sample_status':
    file = pd.read_csv(info, sep=',', header=0)
    mask = file.Type != 'HC'
    # lst = sample.loc[mask == True, 'Sample'].to_list()
elif metaInfo == 'metaInfo':
    file = pd.read_csv(info, sep='\t', header=0)
    mask = file.disease != 'HC'
else:
    print('metaInfo.txt or sample_status.txt not exit in %s' % dataset)

lst = file.loc[mask == True,  file.columns[0]].to_list()


cols = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Frequency']
df = filter_sites(siteType, lst[0])[cols]

for i in lst[1:]:
    if os.path.exists('%s/%s' % (siteType, i)):
        df1 = filter_sites(siteType, i)[cols]
        df = pd.merge(df, df1, how='outer',
                      on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'], suffixes=('', i)).fillna(0)
    else:
        print('%s not exit' % i)
df['MeanFrequency'] = df.iloc[:,5:len(df)].mean(axis=1)
