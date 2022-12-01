# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/4 15:18
# FileName: sites_from_datasites
# Description:


import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to merge sites by datasets, REVISED')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar='directory', required=True,
                    help='The path to the directory contain results')

parser.add_argument('--output', '-o',
                    dest='output', metavar='path',
                    required=True, default='~/projects/upload/database/sites',
                    help='where to save the final file')
args = parser.parse_args()
dirs = args.directory
output = args.output


def mark_dataset(file: str):
    df = pd.read_csv(file, sep='\t', header=0)
    df1 = df.iloc[:, 6:]

    for i in df1.columns:
        mask = df1.loc[:, i].isna()
        df1.loc[:, i][mask == False] = i
    df1 = pd.concat([df.iloc[:, 0:6], df1], axis=1)
    return df1


if __name__ == '__main__':

    files = []
    for i in os.listdir(dirs):
        if i.__contains__('frequency'):
            files.append(i)

    for i in files:
        df = mark_dataset(os.path.join(dirs, i))
        df.to_csv('%s/%s.txt' % (output, i.split('.')[0]), sep='\t', index=None)
