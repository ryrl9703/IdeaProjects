# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesByStatus.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/24 10:14
"""


import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge editing Sites by Status')

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

parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.dirs
status = args.status
opts = args.output



if __name__ == '__main__':

    # os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/remove_chrxym_correct_strand')

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/data/'
                           'metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)
    mask = metaInfo.Disease != 'HC'
    metaInfo.iloc[metaInfo[mask].Disease.index, 3] = 'Patient'


    mask = metaInfo.Disease == status
    lst = metaInfo[mask].Run.to_list()


    df = pd.read_csv('%s/%s.txt' % (dirs, lst[0]), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,3,8]]
    df = df.rename(columns={'Frequency': lst[0]})

    for i in lst[1:]:
        s = pd.read_csv('%s/%s.txt' % (dirs,i), sep='\t', header=0, low_memory=False).iloc[:, [0, 1, 7, 3, 8]]
        s = s.rename(columns={'Frequency': i})

        df = pd.merge(df, s, on=['Region', 'Position', 'AllSubs', 'Strand'], how='outer')
        df = pd.concat([df.iloc[:, 0:4], df.iloc[:, 4:].apply(lambda x: x.dropna().median(), axis=1)], axis=1)
        df = df.rename(columns={df.columns[4]: 'Median_Frequency'})
    df.to_csv('%s/%s.txt' % (opts, status), sep='\t', index=None)