# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/6 8:30
# FileName: allSamplesBases
# Description:


import argparse

import pandas as pd

from utils import find_file

parser = argparse.ArgumentParser(description='scripts to cololect all bam bases')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar='directory',
                    default='/public/workspace/ryrl/projects/rnaedit_autoimmune/data',
                    help='The path to the directory that contains all disease data, default: /public/workspace/ryrl/projects/rnaedit_autoimmune/data')

parser.add_argument('--output', '-o',
                    dest='output', metavar='path',
                    required=True, default='~/projects/upload/database/sites',
                    help='where to save the final file')
args = parser.parse_args()
dirs = args.directory
output = args.output


# def find_file(dirs: str, filename: str) -> str:
#     """
#
#     :param filename:
#     :param dirs:
#     :return:
#     """
#     lst = []
#     for root, dirs, files in os.walk(dirs):
#         for i in files:
#             if i == filename:
#                 lst.append('%s/%s' % (root, i))
#     return lst


if __name__ == '__main__':
    lst = find_file(dirs, 'bases.txt')
    df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
    for i in lst[1:]:
        df1 = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        df = pd.concat([df, df1], axis=0)

    df = df.reset_index(drop=True)
    df.to_csv('%s/AllSampleBases.txt' % output, sep='\t', index=None)
