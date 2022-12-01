# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergEditingSitesByDisease.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/21 08:00
"""
import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory',
                    type= str, required= True,
                    help= 'The path to the directory that contains all sample files')

parser.add_argument('--thread', '-t',
                    dest='thread',
                    metavar= 'number_of_process',
                    default= 10,
                    type= int,
                    help= 'set the number of the thread to run the script')

# parser.add_argument('--disease', '-s',
#                     dest='disease',
#                     metavar= 'disease_name',
#                     type= str, required= True,
#                     help= 'set the number of the thread to run the script')

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
# diss = args.disease


def get_dataset(metaInfo:str, disease:str) -> list:
    """

    :param metaInfo: the metaInfo file
    :param disease: which disease to merge
    :return:
    """
    mask = metaInfo.disease_id == disease
    return list(set(metaInfo[mask == True].dataset))

def merge_dataset(dirs:str, disease:str, dataset: set):
    """

    :param disease:
    :param dirs: directoty contain the edSites by dataset
    :param dataset: the dataset list of the disease
    :return:
    """

    cols = ['chromosome', 'position', 'editing_type']
    for i in dataset[:]:
        if not os.path.exists('%s/%s.txt' % (dirs, i)):
            dataset.remove(i)

    if len(dataset) > 0:
        df = pd.read_csv('%s/%s.txt' % (dirs, dataset[0]), sep='\t', header=0)[cols]
        for i in dataset:
            df1 = pd.read_csv('%s/%s.txt' % (dirs, i), sep='\t', header=0)
            df1 = df1.iloc[:, :len(df1.columns)-8]
            df = pd.merge(df, df1, on=cols, how='outer')
            df.to_csv('%s/%s.tsv' % (opts, disease), sep='\t', index=None)

def main(disease: str):
    """

    :param disease:
    :return:
    """
    dataset = get_dataset(metaInfo, disease)
    merge_dataset(dirs, disease, dataset)


if __name__ == '__main__':

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                           'database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)

    disease = list(set(metaInfo.disease_id))
    mp.Pool(thrd).map(main, disease)
    # dataset = get_dataset(metaInfo, 'RA')
    # for i in dataset:
    #     if not os.path.exists('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/diffSites/fdr/%s.txt' % i):
    #         dataset.remove(i)


    # for i in os.listdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/diffSites/fdr'):
    #     df = pd.read_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/'
    #                                     'database2/rediTable/filtered/diffSites/fdr', i), sep='\t', header=0)
    #     mask = df.cat == 'sig'
    #     df = df[mask == True]
    #     if len(df.index) > 0:
    #         df.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/'
    #                              'database2/rediTable/filtered/diffSites/significant', i), sep='\t', index=None)