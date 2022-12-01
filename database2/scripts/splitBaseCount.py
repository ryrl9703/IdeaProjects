# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : splitBaseCount.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/20 21:15
"""

import os
import sys
import argparse
import pandas as pd
import multiprocessing as mp
sys.path.append('/public/workspace/ryrl/idea/database2/')
from utils import merge_samples

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d',
                    dest='directory',
                    metavar= 'directory',
                    help= 'The path to the directory contains the filtered all samples')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    type= int,
                    metavar= 'number_of_process',
                    default= 10,
                    help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.directory
opts = args.output
thrd = args.thread

def main(dataset:str) -> pd.DataFrame:
    """

    :param dataset:
    :return:
    """
    df = merge_samples(metaInfo, dataset=dataset, column='BaseCount[A,C,G,T]')

    mask = df.Reference == 'A'
    ag = df[mask == True].apply(lambda x: x.str.strip('[]'), axis=1)
    s = ag.iloc[:, 4:].apply(lambda x: x.str.split(',', expand=True)[0].
                             str.cat(x.str.split(',', expand=True)[2], sep=','), axis=1)

    tc = df[mask == False].apply(lambda x: x.str.strip('[]'), axis=1)
    t = tc.iloc[:, 4:].apply(lambda x: x.str.split(',', expand=True)[3].
                             str.cat(x.str.split(',', expand=True)[1], sep=','), axis=1)

    count = pd.concat([s, t], ignore_index=False).sort_index(inplace=False)
    df = pd.concat([df.iloc[:, 0:3], count], axis=1)
    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)

if __name__ == '__main__':

    os.chdir(dirs)
    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                           'database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)
    dataset = metaInfo.dataset.drop_duplicates().reset_index(drop=True).to_list()
    # dataset.remove('GSE171770')
    # dataset.remove('GSE158952')

    mp.Pool(thrd).map(main, dataset)