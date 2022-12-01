# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : dataframe2fasta.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/30 15:17
"""

import argparse
import os

import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description='scripts to transcribe DNA sequence to mRNA')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar='work directory',
                    type=str,
                    required=True,
                    help='The path to the directory that contains the DNA sequence around editing sites')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    metavar='number_of_process',
                    default=10,
                    type=int,
                    help='set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest='output',
                    metavar='path',
                    required=True,
                    help='where to save the final file')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output


def read_file(dirs: str, file: str) -> pd.DataFrame:
    """

    :rtype: object
    :param dirs:
    :param file:
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=None, low_memory=False)

    return df


def cat_columns(df: pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :return:
    """

    s = df.apply(lambda x: x.astype(str), axis=1)
    df = pd.concat([s.apply(lambda x: x[:-1].str.cat(sep='|'), axis=1), s.iloc[:, -1]], axis=1)
    df = df.rename(columns={df.columns[0]: 'header', df.columns[1]: 'mRNA'})
    df.header = '>' + df.header

    df = df.header.str.cat(df.mRNA, sep='_').str.split('_').explode(ignore_index=True)  # explode to two rows

    return df


def main(dirs: str, file: str):
    """

    :param dirs:
    :param file:
    :return:
    """

    df = read_file(dirs, file)
    df = cat_columns(df)

    df.to_csv('%s/%s.fasta' % (opts, file.split('.')[0]), sep='\t', index=False, header=False)


if __name__ == '__main__':
    # os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/unedited')
    #

    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/edited/ori'
    # thrd = 30
    # opst = '/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/unedited/fasta'
    # lst = os.listdir(dirs)

    # df = pd.read_csv('%s/%s' % (dirs, lst[0]), sep='\t', header=None, low_memory=False)

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(main, args=(dirs, i))
    pool.close()
    pool.join()
