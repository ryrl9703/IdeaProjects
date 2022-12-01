# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : AluElementCounts.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/1 14:22
"""

import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description= 'scripts to count the Alu Elements')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the cis-NATs intersect with edSites')

# parser.add_argument('--status', '-s',
#                     dest='status',
#                     metavar= 'status',
#                     type= str,
#                     required= True,
#                     choices=['HC', 'PA'],
#                     help= 'The status of the samples')


parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.dirs
opts = args.output
# status = args.status


def count_AluElement(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """
    # df = pd.read_csv('%s/%s.tsv' % (dirs1, disease), sep='\t', header=0, low_memory=False)
    # df.rmsk_tid.str.split('-', expand=True)[0].value_counts()

    cis = pd.read_csv('%s/%s.bed' % (dirs, file), sep='\t', header=None, low_memory=False)
    s = pd.DataFrame(cis[cis.columns[25]].str.split('-', expand=True)[0].value_counts())
    s = s.rename(columns={s.columns[0]: file.split('.')[0]})
    return s

def main(dirs:str) -> pd.DataFrame:
    """

    :param dirs:
    :return:
    """

    lst = os.listdir(dirs)
    df = pd.DataFrame()

    for i in lst:
        s = count_AluElement(i.split('.')[0])
        df = pd.concat([df, s], axis=1)

    df = df.fillna(value=0)
    # df.columns = df.columns.str.split('_')[0]
    df.index.names = ['Elements']
    df.T.to_csv('%s/%s_%s.tsv' % (opts,'cis_NATs_elements', dirs.split('/')[-1]), sep='\t', index=True)

    return df



if __name__ == '__main__':

    df = main(dirs=dirs)
