# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : rna_edited.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/21 14:43
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description='scripts to edit the mRNA sequence')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar='work directory',
                    type=str,
                    required=True,
                    help='The path to the directory that contains the transcribed mRNA sequence')

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


def edit_sequence(dirs:str, file: str) -> None:
    """

    :type dirs:
    :param dirs:
    :param file:
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=None, low_memory=False)

    edited = pd.DataFrame(
        df.apply(lambda x: x[8][:49] + 'G' + x[8][51:] if x[3] == 'A' else x[8][:49] + 'C' + x[8][51:], axis=1)
    )

    df = pd.concat([df, edited], axis=1)
    df.to_csv('%s/%s' % (opts, file), sep='\t', header=False, index=False)
    return None


if __name__ == '__main__':

    # df = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/unedited/SRR6730168.tsv', sep='\t', header=None, low_memory=False)
    #
    # # df.iloc[0, 8] = df.iloc[0, 8][:49] + ' G ' + df.iloc[0, 8][51:]
    #
    # df = pd.concat([df, pd.DataFrame(df.apply(lambda x: x[8][:49] + 'G' + x[8][51:] if x[3] == 'A' else x[8][:49] + 'C' + x[8][51:], axis=1))], axis=1)

    lst = os.listdir(dirs)
    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(edit_sequence, args=(dirs, i))
    pool.close()
    pool.join()
