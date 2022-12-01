# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeEditingSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/20 09:19
"""

import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory',
                    default= '/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/ori',
                    help= 'The path to the directory that contains all sample files,'
                          'default: /public/workspace/ryrl/projects/upload/database2/rediTable/filtered/ori')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    metavar= 'number_of_process',
                    default= 10,
                    type= int,
                    help= 'set the number of the thread to run the script')

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.directory
opts = args.output
thrd = args.thread



def merge_dataset(dir: str, srr: list) -> pd.DataFrame:
    """

    :param dir:
    :param srr:
    :return:
    """

    df = pd.read_csv('%s/%s/%s.tsv' % (dir, srr[0], srr[0]),
                     sep='\t', header=0)[['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Frequency']]
    df = df.rename(columns={'Frequency': srr[0]})
    for i in srr[1:]:
        cols = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'Frequency']
        df1 = pd.read_csv('%s/%s/%s.tsv' % (dir, i, i), sep='\t', header=0)[cols]
        df1 = df1.rename(columns={'Frequency': i})
        cols.remove('Frequency')
        df = pd.merge(df, df1,how='outer', on= cols)
    return df

def run_merge(dataset: str) -> pd.DataFrame:
    """

    :param dataset:
    :return:
    """

    mask = metaInfo.dataset == dataset
    s = metaInfo[mask == True].Run.to_list()

    if 'SRR15372438' in s: s.remove('SRR15372438')

    df = merge_dataset(dir= dirs, srr= s)
    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)

if __name__ == '__main__':

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)
    dataset = metaInfo.dataset.drop_duplicates().reset_index(drop=True).to_list()

    # mask = metaInfo.dataset == i
    # s = metaInfo[mask == True].Run.to_list()
    #
    # if 'SRR15372438' in s: s.remove('SRR15372438')
    mp.Pool(thrd).map(run_merge, dataset)