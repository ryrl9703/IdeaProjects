# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesFrequencyByDiseaseStatus.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/23 10:04
"""

import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to calculate regulatory genes')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains editing sites each sample')

parser.add_argument('--status', '-s',
                    dest='status',
                    metavar= 'status',
                    type= str,
                    choices=['HC', 'Patient'],
                    help= 'The status of the samples, choose from HC or Patient')


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

def get_sample_byDisease(metaInfo:pd.DataFrame, dis:str, status:str) -> list:
    """

    :param metaInfo:
    :param dis:
    :param status:
    :return:
    """

    mask = metaInfo.Disease_id == dis
    samples = metaInfo[mask]

    if status not in set(samples.Disease):
        print('%s have no %s sample' % (dis, status))
    else:
        mask = samples.Disease == status
        lst = samples[mask].Run.to_list()

        return lst


def merge_frequency(metaInfo:pd.DataFrame, dis:str) -> pd.DataFrame:
    """

    :param metaInfo:
    :param dis:
    :return:
    """

    lst = get_sample_byDisease(metaInfo, dis, status)
    df = pd.read_csv('%s/%s.txt' % (dirs, lst[0]), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,3,8]]
    df = df.rename(columns={'Frequency': lst[0]})

    for i in lst[1:]:
        s = pd.read_csv('%s/%s.txt' % (dirs, i), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,3,8]]
        s = s.rename(columns={'Frequency': i})

        df = pd.merge(df, s, on=['Region', 'Position', 'AllSubs', 'Strand'], how='outer')

        df = pd.concat([df.iloc[:, 0:4], df.iloc[:, 4:].apply(lambda x: x.dropna().median(), axis=1)], axis=1)
        df = df.rename(columns={df.columns[4]: 'Median_Frequency'})

    df.to_csv('%s/%s.tsv' % (opts, dis), sep='\t', index=False)
    return df



if __name__ == '__main__':

    # dis = 'Coeliac'
    # status = 'HC'
    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/remove_chrxym_correct_strand'
    # opts = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Frequency/Diseases/HC'
    # thrd = 7


    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/data/'
                           'metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)
    mask = metaInfo.Disease != 'HC'
    metaInfo.iloc[metaInfo[mask].Disease.index, 3] = 'Patient'

    disease = list(set(metaInfo.Disease_id))

    pool = mp.Pool(thrd)
    for i in disease:
        pool.apply_async(merge_frequency, args=(metaInfo, i))
    pool.close()
    pool.join()