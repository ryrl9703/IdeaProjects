# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/10 10:25
# FileName: geneEditedTpmMergeEditedSites
# Description:


import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description= 'scripts to cololect all bam bases')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory',
                    default= '/public/workspace/ryrl/projects/upload/database/results/genesEditedTpmByDataSet',
                    help= 'The path to the directory that contains all disease data, default: /public/workspace/ryrl/projects/upload/database/results/genesEditedTpmByDataSet')

parser.add_argument('--path', '-p', dest='path',
                    metavar= 'directory',
                    default= '/public/workspace/ryrl/projects/upload/database/results/geneAnno/results',
                    help= 'The directory store the geneAnnotation, default:/public/workspace/ryrl/projects/upload/database/results/geneAnno/results')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dirs = args.directory
# file = args.file
path = args.path
output = args.output


def mergeSites(dirs:str, file:str, path:str) -> pd.DataFrame:
    """

    :param path:
    :param file:
    :param dirs:
    :return:
    """

    tpm = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=0, index_col=0)
    df = pd.read_csv('%s/%s.variant_function' % (path, file.split('_')[0]),
                     sep='\t', header=0)
    df['genes'] = df['genes'].str.split(',')
    df = df.explode('genes')
    df = pd.merge(df, tpm, left_on=['genes'], right_index=True, how='left')
    return df


if __name__ == '__main__':

    lst = os.listdir(dirs)

    for i in lst:
        df = mergeSites(dirs, i, path)
        df.to_csv('%s/%s_%s' % (output, i.split('_')[0], i.split('_')[1]), sep='\t', index=None)
