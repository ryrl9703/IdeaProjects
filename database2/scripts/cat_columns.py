# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/5 8:33
# FileName: cat_columns
# Description:


import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description= 'scripts to cat the columns')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory', required= True,
                    help= 'The path to the directory contain results')


parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dirs = args.directory
output = args.output


def cat_columns(file: str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """

    df = pd.read_csv(file, sep='\t', header=0, low_memory=False)
    df = df.fillna('-')
    lst = df.columns[6:]
    for i in lst[1:]:
        df[lst[0]] = df[lst[0]].str.cat(df[i], sep=';')

    df[lst[0]] = df[lst[0]].str.replace('-;', '').str.replace(';-', '')
    df = df.iloc[:, 0:7]
    df = df.rename(columns={lst[0]: 'samples'})
    return df


if __name__ == '__main__':
    files = os.listdir(dirs)

    for i in files:
        df = cat_columns(os.path.join(dirs, i))
        df.to_csv('%s/%s.txt' % (output, i.split('.')[0]), sep='\t', index=None)