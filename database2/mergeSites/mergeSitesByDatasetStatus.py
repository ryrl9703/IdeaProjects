# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesByDatasetStatus.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/18 08:28
"""


import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to calculate regulatory genes')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the datasets')

parser.add_argument('--ststus', '-s',
                    dest='status',
                    metavar= 'status',
                    choices=['HC', 'Patient'],
                    type= str,
                    required=True,
                    help= 'The status of the sample, choose from "HC" and "Patient"')

# parser.add_argument('--columns', '-c',
#                     dest='columns',
#                     metavar= 'columns',
#                     type= str,
#                     required=False,
#                     help= 'The columns that you want to select to merge')

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
status = args.status
thrd = args.thread
opts = args.output

def get_sample(metaInfo:pd.DataFrame, dataset:str, status:str) -> list:
    """

    :param dataset: the name of the data set
    :param metaInfo:
    :param status: 'HC'
    :return: sample name list
    """

    mask = metaInfo.Dataset == dataset
    samples = metaInfo[mask]
    if status not in set(samples.Disease):
        print('%s have no %s sample' % (dataset, status))
    else:
        mask = samples.Disease == status
        lst = samples[mask].Run.to_list()

        return lst

def mergeSites(dirs:str, metaInfo:pd.DataFrame,
               dataset:str, opts:str, status:str) -> pd.DataFrame:
    """

    :param opts: the directory to strore the merged Editing Sites
    :param status: the status of samples
    :param metaInfo:
    :param dirs:
    :param dataset:
    :return:
    """

    lst = get_sample(metaInfo, dataset, status)
    if len(lst) > 0:
        for i in lst[:]:
            if not os.path.exists('/public/workspace/ryrl/projects/upload/database3/data/ori/%s' % i):
                lst.remove(i)


        cols = ['Region', 'Position', 'Strand', 'AllSubs','Frequency']
        df = pd.read_csv('%s/%s/%s.tsv' % (dirs, lst[0], lst[0]),
                         sep='\t', header=0, low_memory=False)[cols[0:4]]

        for j in lst[1:]:

            df1 = pd.read_csv('%s/%s/%s.tsv' % (dirs, j, j), sep='\t', header=0, low_memory=False)[cols]
            df1 = df1.rename(columns={'Frequency': j})  # rename frequency columns to the sample name
            df = pd.merge(df, df1, on=cols[0:4], how='outer')

        df.to_csv('%s/%s_%s.tsv' % (opts, dataset, status), sep='\t', index=None)
    else:
        print('%s has no sample with %s' % (dataset, status))
    return None




if __name__ == '__main__':

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/'
                           'upload/database3/data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)
    mask = metaInfo.Disease != 'HC'
    metaInfo.iloc[metaInfo[mask].Disease.index, 3] = 'Patient'

    pool = mp.Pool(thrd)
    for i in set(metaInfo.Dataset):
        pool.apply_async(mergeSites, args=[dirs, metaInfo, i, opts, status])
    pool.close()
    pool.join()