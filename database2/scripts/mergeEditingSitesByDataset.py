# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeEditingSitesByDataset.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/22 22:21
"""

import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d',
                    dest='directory',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains all sample files')

parser.add_argument('--status', '-s',
                    dest='status',
                    metavar= 'status',
                    type= str,
                    required= False,
                    help= 'The status of the sample you want to use')

parser.add_argument('--thread', '-t',
                    metavar= 'number_of_process',
                    dest='thread',
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
stat = args.status


def merge_editingSitesByDataset(dirs:str, sample:list, col:str =None) -> pd.DataFrame:
    """

    :param dirs: the directory where store the all filtered editing sites
    :param sample: the list of the needed samples in a dataset
    :param col: which column you want to keep, default: None
    :return:
    """

    columns = ['Region', 'Position', 'Reference', 'Strand', 'AllSubs']
    df = pd.read_csv('%s/%s/%s.tsv' % (dirs, sample[0], sample[0]), sep='\t', header=0)[columns]

    for i in sample:
        if col is not None:
            columns.append(col)
            df1= pd.read_csv('%s/%s/%s.tsv' % (dirs, i, i), sep='\t', header=0)[columns]
            df = df.rename(columns= {col: i})
            columns.remove(col)
            df = pd.merge(df, df1, how='outer', on=columns)
        else:
            df1 = pd.read_csv('%s/%s/%s.tsv' % (dirs, i, i), sep='\t', header=0)[columns]
            df = pd.merge(df, df1, how='outer', on=columns)
    return df

def select_sample(metaInfo:str, dataset:str, status: str=None) -> list:
    """

    :param dataset: the name of the dataset
    :param metaInfo: the file of the metaInfo contain all samples
    :param status: the status of the sample, default: 'HC'
    :return: the sample list to be used
    """

    if status is not None:
        metaInfo = metaInfo[metaInfo.disease != status]
    samples = metaInfo[metaInfo.dataset == dataset].Run.to_list()
    return samples

def main(dataset:str):
    """

    :param dataset:
    :return:
    """

    sample = select_sample(metaInfo, dataset, stat)
    df = merge_editingSitesByDataset(dirs, sample, col='Coverage-q30')
    df.to_csv('%s/%s.tsv' % (opts, dataset), sep='\t', index=None)
    return

if __name__ == '__main__':
    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                           'database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)
    dataset = metaInfo.dataset.drop_duplicates().reset_index(drop=True).to_list()

    with mp.Pool(thrd) as p:
        p.map(main, dataset)
        p.close()
        p.join()

    # df = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/'
    #                  'rediTable/filtered/mergeSitesByDataset/annotation/snp151/'
    #                  'GSE103489.tsv.refGene.rmsk.snp151.txt', sep='\t', header=0)
    #
    # df.rmsk_tid.value_counts()
    # df.refGene_feat.str.split(',', expand=True)[0].value_counts()