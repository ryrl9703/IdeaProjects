# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/4 18:46
# FileName: site_merge_revised
# Description:
# metaInfo.number1 = test[0].str.cat(test[1].str.zfill(4), sep='-')
# df.to_csv('/public/workspace/ryrl/projects/upload/database/metaInfo_all.txt', sep='\t', index=None)

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to merge sites by datasets, REVISED')

parser.add_argument('--redi', '-r', dest='redi',
                    metavar='redi path', required=True,
                    help='The path to the directory contain reditools results')

parser.add_argument('--recoding', '-c', dest='recoding',
                    metavar='recoding path', required=True,
                    help='The path to the directory contain reditools recoding results')

parser.add_argument('--metaInfo', '-m',
                    dest='metaInfo',
                    metavar='sample information',
                    default='/public/workspace/ryrl/projects/upload/database/results/metaInfo/metaInfo_all.txt',
                    help='The file that contain sample information, choose from metaInfo and sample_status,'
                         'default: /public/workspace/ryrl/projects/upload/database2/metaInfo/metaInfo_add_ISG.txt')

parser.add_argument('--output', '-o',
                    dest='output', metavar='directory', required=True,
                    help='where to save the dataset final file')

args = parser.parse_args()
path = args.redi
reco = args.recoding
metaInfo = args.metaInfo
output = args.output


def find_number(metaInfo, sample):
    """

    :param sample: sample id
    :param metaInfo: file contains all samples and information
    :return:
    """
    for index, srr in enumerate(metaInfo.Run):
        if sample in list(metaInfo.Run) and sample == srr:
            return metaInfo.disease_dataset_sample[index]


def cat_sites_sampleId(path, sample):
    """

    :param path: path to the site file
    :param sample:  the sample name
    :return:
    """
    df = pd.read_csv(path, sep='\t', header=0)
    df['sample_id'] = find_number(metaInfo, sample)
    df['Frequency'] = df['Frequency'].astype(str).str.cat(df['sample_id'], sep='-')
    df = df.drop(
        columns=['Coverage-q30', 'gCoverage-q30', 'gMeanQ', 'gBaseCount[A,C,G,T]',
                 'MeanQ', 'BaseCount[A,C,G,T]', 'gAllSubs', 'gFrequency', 'sample_id'])
    return df


def split_BaseCount(file):
    df = pd.read_csv(file, sep='\t', header=0)
    mask = df.AllSubs == 'AG'
    if df.shape[0] >= 2:
        ag = df[mask == True]
        tc = df[mask != True]
        ag['BaseCount[A,C,G,T]'] = ag['BaseCount[A,C,G,T]']. \
            str.strip('[]').str.split(',', expand=True)[2].str.replace(' ', '')
        tc['BaseCount[A,C,G,T]'] = tc['BaseCount[A,C,G,T]']. \
            str.strip('[]').str.split(',', expand=True)[1].str.replace(' ', '')
        df = pd.concat([ag, tc])
    else:
        print('====Only one site in %s, drop====' % file.split('/')[-1])
    return df


def merge_files(path: str, metaInfo=None, sitetype: str = 'redi'):
    """


    :param path: path to the directory contain all sample file directory
    :param metaInfo: file contains all samples and information
    :param sitetype:
    :return:
    """
    lst = os.listdir(path)
    cols = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Coverage-q30', 'BaseCount[A,C,G,T]', 'Frequency']
    cols1 = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs']
    if sitetype == 'redi':
        if metaInfo is not None:
            # df = cat_sites_sampleId('%s/%s/%s.tsv' % (path, lst[0], lst[0]), lst[0])
            df = split_BaseCount('%s/%s/%s.tsv' % (path, lst[0], lst[0]))[cols]
            sampleId = find_number(metaInfo, lst[0])
            df = df.rename(
                columns={'Frequency': 'Frequency' + '_%s' % sampleId,
                         'Coverage-q30': 'Coverage-q30' + '_%s' % sampleId,
                         'BaseCount[A,C,G,T]': 'BaseCount[A,C,G,T]' + '_%s' % sampleId})
            for i in lst[1:]:
                # df1 = cat_sites_sampleId('%s/%s/%s.tsv' % (path, i, i), i)
                df1 = split_BaseCount('%s/%s/%s.tsv' % (path, i, i))[cols]
                sampleId = find_number(metaInfo, i)
                df1 = df1.rename(
                    columns={'Frequency': 'Frequency' + '_%s' % sampleId,
                             'Coverage-q30': 'Coverage-q30' + '_%s' % sampleId,
                             'BaseCount[A,C,G,T]': 'BaseCount[A,C,G,T]' + '_%s' % sampleId})
                df = pd.merge(df, df1, how='outer',
                              on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'])
            # df = df.fillna(0)
            # df.columns = df.columns.str.replace('Frequency_', '')
            return df
        else:
            print('meatInfo not exit, please check!')
    else:

        df = pd.read_csv('%s/%s/%s' % (path, lst[0], lst[0]), sep='\t', header=0)[cols1]
        for i in lst[1:]:
            df1 = pd.read_csv('%s/%s/%s' % (path, i, i), sep='\t', header=0)[cols1]
            df = pd.merge(df, df1, how='outer', on=cols1)
        # mask = df.AllSubs == '-'
        df['type'] = 'recoding'
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

    df = df[['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Frequency']]
    df.Frequency = df.Frequency.str.replace('-;', '').str.replace(';-', '')
    return df


def mark_recoding(recoding: pd.DataFrame, redi: pd.DataFrame):
    df = pd.merge(recoding, redi, how='right',
                  on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'])
    df.type = df.type.fillna('-')
    return df


if __name__ == '__main__':
    metaInfo = pd.read_csv(metaInfo, sep='\t', header=0)
    redi = merge_files(path, metaInfo)
    # redi = cat_frequency(redi)

    recoding = merge_files(reco, sitetype='recoding')
    df = mark_recoding(recoding, redi)
    df.to_csv('%s/%s.txt' % (output, path.split('/')[0]), sep='\t', index=None)
