# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/5 19:28
# FileName: frequency_gene
# Description:


import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to collect the BAM bases')

parser.add_argument('--directory1', '-d1', dest='directory',
                    metavar= 'directory', required= True,
                    help= 'The path to the directory contain frequency')

parser.add_argument('--directory2', '-d2', dest='dirs',
                    metavar= 'directory', required= True,
                    help= 'The path to the directory contain annotation')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dir1 = args.directory
dir2 = args.dirs
output = args.output


def contact_gene(file1:str, file2:str) -> pd.DataFrame:
    """

    :param file1:
    :param file2:
    :return:
    """

    df = pd.read_csv(file1, sep='\t', header=0, low_memory=False)
    gene = pd.read_csv(file2, sep='\t', header=0)['Gene_refGene']
    df = pd.concat([df.iloc[:, 0:6], gene, df.iloc[:,6:]], axis=1)
    return df


if __name__ == '__main__':
    for i in os.listdir(dir1):
        df = contact_gene('%s/%s' % (dir1, i), '%s/%s' % (dir2, i))
        df.to_csv('%s/%s' % (output, i), sep='\t', index=None)