# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeMatrix.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/9 10:30
"""

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge the matrix of APA PDUI')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains all matrix')

# parser.add_argument('--thread', '-t',
#                     dest='thread',
#                     metavar= 'number_of_process',
#                     default= 10,
#                     type= int,
#                     help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file, a directory')

args = parser.parse_args()

dirs = args.dirs
# thrd = args.thread
opts = args.output


def get_matrix_path(dirs:str) -> list:
    """

    :param dirs:
    :return:
    """
    lst = []

    for root, directory, files in os.walk(dirs):
        for i in files:
            lst.append('%s/%s' % (root, i))
    return lst

def process_matrix(path:str) -> pd.DataFrame:
    """

    :param path: the path and the file name to the file
    :return: file processed
    """

    mat = pd.read_csv(path, sep='\t', header=0, low_memory=False)
    mat[['Transcript_id', 'Symbol', 'Chr', 'Strand']] = mat.Gene.str.split('|', expand=True)
    mat = pd.concat([mat.iloc[:, 0:4],
                     mat.iloc[:, mat.shape[1] - 4:mat.shape[1]],
                     mat.iloc[:, 4:(mat.shape[1] - 4)]], axis=1)
    return mat

def main() -> pd.DataFrame:
    """

    :return: None
    """
    lst = get_matrix_path(dirs=dirs)
    df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
    de = df.iloc[:, 0:4]

    for i in lst[1:]:
        s = pd.read_csv(i, sep='\t', header=0, low_memory=False)

        de = pd.merge(de, s.iloc[:, 0:4], how='outer', on=['Gene'],
                      suffixes=('', '_%s' % i.split('/')[-2].split('_')[0]))

        df = pd.merge(df.drop(columns=df.columns[1:4]),
                      s.drop(columns=s.columns[1:4]), how='outer', on=['Gene'])

    de.to_csv('%s/position.tsv' % (opts, ), sep='\t', index=None)
    df.to_csv('%s/PDUI.tsv' % (opts, ), sep='\t', index=None)

    return










if __name__ == '__main__':
    # os.chdir('/public/workspace/xyyang0826/xyyang/DaPars2.1/DaPars2_combined_all_chromosome/SLE_scRNA-seq/GSE137029/healthy')
    #
    # dirs = './'
    # df = pd.read_csv('./0831_1/combined_chr_20220825.txt', sep='\t', header=0, low_memory=False)
    # df[['Transcript_id', 'Symbol', 'Chr', 'Strand']] = df.Gene.str.split('|', expand=True)
    # df = pd.concat([df.iloc[:, 0:4], df.iloc[:, df.shape[1]-4:df.shape[1]], df.iloc[:, 4:(df.shape[1]-4)]], axis=1)

    main()

    # len('TGTCACCCAGACTGGAGTGCAGTAGCATGATCTCAGCTCACTGCAGCCTTGACCTCCCTGCCTCAAGCAATCCTCCTATCTCAGCCTCCCAAGTAGCTTAG')