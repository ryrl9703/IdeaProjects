# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : contactRediAnnovar.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/23 13:26
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--redi', '-d',
                    dest='redi',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the annotation results of AnnotateTable')

parser.add_argument('--anno', '-a',
                    dest='anno',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the annotation results of Annovar')


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
redi = args.redi
anno = args.anno
thrd = args.thread
opts = args.output

def contact_rediAnnovar(redi_dir:str, annovar_dir:str, sample:str, out:str):
    """

    :param sample: sample name
    :param redi_dir: reditools AnnotateTable results
    :param annovar_dir: annovar annotation results
    :param out: where to save the final results
    :return:
    """

    redi = pd.read_csv('%s/%s' % (redi_dir, sample), sep='\t', header=0)
    anno = pd.read_csv('%s/%s' % (annovar_dir, sample), sep='\t', header=0)
    df = pd.concat([redi, anno.iloc[:, 5:]], axis=1)
    df.to_csv('%s/%s' % (out, sample), sep='\t', index=None)


if __name__ == '__main__':

    lst = os.listdir(redi)
    pool = mp.Pool(thrd)
    for i in lst:
        # print(i)
        pool.apply_async(contact_rediAnnovar, args=[redi, anno, i, opts])  # 多个参数的时候用[]
    pool.close()
    pool.join()

    # os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/mergeSitesByDataset/results')
    # lst = os.listdir('./contact')
    #
    # for i in lst:
    #     df = pd.read_csv('./contact/%s' % i, sep='\t', header=0)
    #     df.rmsk_tid = df.rmsk_tid.str.split('-', expand=True)[0]
    #     df = df.loc[:, ['Gene_refGene', 'rmsk_tid']]
    #     df['Gene_refGene'] = df['Gene_refGene'].str.split(';')
    #     df = df.explode('Gene_refGene')
    #     df.groupby('Gene_refGene').count()
    #     df = df.rename(columns={'rmsk_tid': i})