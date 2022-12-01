# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/6 9:18
# FileName: GeneRNAAbundances
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to cololect all bam bases')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory',
                    default= '/public/workspace/ryrl/projects/rnaedit_autoimmune/data',
                    help= 'The path to the directory that contains all disease data, default: /public/workspace/ryrl/projects/rnaedit_autoimmune/data')


parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dirs = args.directory
output = args.output

def find_file(dirs:str, filename:str) -> str:
    """

    :param filename:
    :param dirs:
    :return:
    """
    lst = []
    for root, dirs, files in os.walk(dirs):
        for i in files:
            if i == filename:
                lst.append('%s/%s' % (root, i))
    return lst


def editGenes(dirs:str) -> pd.DataFrame:

    lst = os.listdir(dirs)
    df = pd.read_csv('%s/%s' % (dirs, lst[0]), sep='\t', header=0, low_memory=False)
    genes = df['Gene_refGene'].str.split(';').explode().drop_duplicates()
    for i in lst[1:]:
        df1 = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0, low_memory=False)
        genes = pd.concat([genes,
                           df1['Gene_refGene'].str.split(';').explode().drop_duplicates()], axis=0)
    genes = genes.str.split(';').explode().drop_duplicates()
    return genes

def editGenesDisease(file:str) -> pd.DataFrame:

    df = pd.read_csv(file, sep='\t', header=0, low_memory=False)
    genes = df['Gene_refGene'].str.split(';').explode()
    return genes




if __name__ == '__main__':
    for i in os.listdir(dirs):
        genes = editGenesDisease('%s/%s' % (dirs, i))
        genes.to_csv('%s/%s' % (output, i), sep='\t', index=None)