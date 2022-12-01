# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : IFNScore.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/18 17:16
"""

import os
# import sys
import argparse
import numpy as np
import pandas as pd

# sys.path.append('/public/workspace/ryrl/idea/database2')
# from utils import find_file, modified_zscore

parser = argparse.ArgumentParser(description='scripts to calculate ISG scores')

parser.add_argument('--directory', '-d',
                    dest='dir',
                    metavar='directory',
                    required=True,
                    help='The directory contains the Tpm of the dataset')

# parser.add_argument('--tpm', '-t',
#                     dest='tpm',
#                     metavar='tpm',
#                     required=True,
#                     help='The name of the tpm file')

parser.add_argument('--metaInfo', '-m',
                    dest='metaInfo',
                    metavar='metaInfo',
                    required=True,
                    help='The path to the metaInfo')

parser.add_argument('--output', '-o',
                    dest='output',
                    metavar='path',
                    required=True,
                    help='where to save the final file')

args = parser.parse_args()
dirs = args.dir
# tpm = args.tpm
metaInfo = args.metaInfo
opts = args.output


# def find_file(dirs: str, filename: str) -> list[str]:
#     """
#
#     :param filename: the name of the file
#     :param dirs: directory where store the file that you want to find
#     :return: a list of the path to the file
#     """
#     lst = []
#     for root, dirs, files in os.walk(dirs):
#         for i in files:
#             if i == filename:
#                 lst.append('%s/%s' % (root, i))
#     return lst


def modified_zscore(col: pd.Series) -> pd.Series:
    """

    :param col: the col
    :return:
    """
    mid = col.median()
    mid_abs_dev = (np.abs(col - mid)).median()
    mod_zscore: float = 0.6745 * ((col - mid) / mid_abs_dev)
    return mod_zscore

def main(dirs:str, opts:str):
    """

    :param dirs: directory contain the file of the TPM of dataset
    :param opts: directory to store the finall results
    :return: the finall modified zscore data frame
    """
    lst = os.listdir(dirs)
    genes = pd.Series(['IFI27', 'IFI44L', 'IFIT1', 'ISG15', 'RSAD2', 'SIGLEC1'])
    df = pd.DataFrame()

    for i in lst:
        tpm = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0, index_col=0, low_memory=False)

        if set(genes).issubset(tpm.index):
            isg = tpm.loc[genes, :].T

            mod_z = isg.apply(modified_zscore, axis=0)
            mod_z['IFN_score'] = mod_z.sum(axis=1)

            df = pd.concat([df, pd.DataFrame(mod_z['IFN_score'])])
        else:
            print('%s cannot calculate modified_zscore' % i)
    df.index.names = ['Run']
    # df.to_csv('%s/IFN_score.txt' % (opts,), sep='\t', index=True)

    return df


if __name__ == '__main__':

    df = main(dirs, opts)
    metaInfo = pd.read_csv(metaInfo, sep='\t', header=0, low_memory=False)
    metaInfo = pd.merge(metaInfo, df, how='left', left_on=['Run'], right_index=True)
    metaInfo.to_csv('%s/metaInfo_HallMark_IFNscore.txt' % opts, sep='\t', index=None)
