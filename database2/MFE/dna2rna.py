# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : dna2rna.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/17 18:00
"""

import os
import argparse
import numpy as np
import pandas as pd
from Bio.Seq import Seq
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


def get_mrna(dirs: str, file: str) -> None:
    """

    :param dirs:
    :param file:
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=None, low_memory=False)

    mask = df[6] == 'UTR3'
    df = df[mask].reset_index(drop=True)
    mask = df[4] == '+/-'
    df = df[mask == False].reset_index(drop=True)

    array = np.array([])
    for ind, dat in df.iterrows():
        if dat[4] == '+':
            array = np.append(array, str(Seq(dat[7]).transcribe()))
        else:
            array = np.append(array, str(Seq(dat[7]).reverse_complement().transcribe()))
    array = array.reshape(-1, 1)

    df = pd.concat([df, pd.DataFrame(array, columns=['rna'])], axis=1)

    df.to_csv('%s/%s' % (opts, file), sep='\t', index=False, header=False)

    return None


if __name__ == '__main__':

    # os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/genome_fasta')
    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/genome_fasta'
    # file = 'SRR8312310.tsv'
    # opts = '/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/unedited'
    # df1 = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Seqcence/unedited/SRR8312310.tsv', sep='\t', header=0, low_memory=False)

    lst = os.listdir(dirs)

    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(get_mrna, args=(dirs, i))
    pool.close()
    pool.join()
