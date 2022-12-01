# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergRecodingByDataset.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/16 02:52
"""


import os
import pandas as pd
import argparse
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to calculate regulatory genes')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the datasets')


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
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output

def merge_recoding(dirs:str, metaInfo:pd.DataFrame, dataset:str, opts:str) -> pd.DataFrame:
    """

    :param dataset:
    :param opts:
    :param dirs:
    :param metaInfo:
    :return:
    """

    mask = metaInfo.Dataset == dataset
    lst = metaInfo.loc[mask, 'Run'].to_list()

    for s in lst[:]:
        if not os.path.exists('%s/%s/%s.tsv' % (dirs, s)):
            lst.remove(s)

    cols = ['Region', 'Position', 'AllSubs']
    df = pd.read_csv('%s/%s.tsv' % (dirs, lst[0]), sep='\t', header=0)[cols]

    for j in lst[1:]:
        df1 = pd.read_csv('%s/%s.tsv' % (dirs, j), sep='\t', header=0)[cols]
        df = pd.merge(df, df1, on=cols, how='outer')
    df.to_csv('%s/%s.txt' % (opts, dataset), sep='\t', index=None)
    return


if __name__ == '__main__':

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                           'database3/data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)

    lst1 = set(metaInfo.Dataset)

    pool = mp.Pool(thrd)
    for i in lst1:
        pool.apply_async(merge_recoding, args=[dirs, metaInfo, i, opts])
    pool.close()
    pool.join()

    # metaInfo = pd.read_csv('/public/workspace/ryrl/projects/'
    #                        'upload/database3/data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)
    # mask = metaInfo.Dataset == 'GSE89408'
    # lst = metaInfo.loc[mask, 'Run'].to_list()
    #
    # cols = ['Region', 'Position', 'AllSubs']
    # df = pd.read_csv('%s/%s.tsv' % ('filtered', lst[0]), sep='\t', header=0)
    # mask = metaInfo.Disease == 'HC'
    # m = metaInfo[mask].iloc[:, 2].reset_index(drop=True)
    # t = metaInfo[mask == False].iloc[:, 2].reset_index(drop=True)
    # df = pd.concat([m,t], axis=1)
    # df.to_csv('/public/workspace/ryrl/projects/upload/test.txt', sep='\t', index=None)

    os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/mergeSitesByDataset/sites_frequency/filteredBySampleNumber')

    lst = os.listdir('./')

    df = pd.read_csv(lst[0], sep='\t', header=0).iloc[:, 0:3]

    for i in lst:
        df1 = pd.read_csv(i, sep='\t', header=0).drop(columns=['samplesSupport'])
        df = pd.merge(df, df1, on=['Region', 'Position', 'AllSubs'], how='outer')