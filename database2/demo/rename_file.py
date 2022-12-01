# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : rename_file.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/23 19:33
"""

import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to merge Editing Sites')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory',
                    type= str, required= True,
                    help= 'The path to the directory where the script to work')

parser.add_argument('--metaInfo', '-m',
                    dest='metaInfo',
                    metavar= 'path',
                    type= str,
                    help= 'the path to the metaInfo file')


# parser.add_argument('--output', '-o',
#                     dest= 'output',
#                     metavar= 'path',
#                     required=True,
#                     default= '~/projects/upload/database/sites',
#                     help= 'where to save the final file')

args = parser.parse_args()

dirs = args.directory
meta = args.metaInfo
# opts = args.output

def get_disease(path:str, dataset:str):
    """

    :param path: path to the metaInfo file
    :param dataset: the name of the dataset
    :return:  disease name
    """


    metaInfo = pd.read_csv(path, sep='\t', header=0).\
                   loc[:, ['dataset', 'disease_id', 'sample_type']].drop_duplicates().reset_index(drop=True)

    for index, dat in enumerate(metaInfo.dataset):
        if dat == dataset:
            return metaInfo.disease_id[index], metaInfo.sample_type[index]

def main(dirs:str, dataset:str, path:str):
    """

    :param dirs:
    :param dataset:
    :param path:
    :return:
    """

    os.chdir(dirs)
    dis, type = get_disease(path, dataset)
    os.system('mv %s_%s.txt %s_%s_%s.txt' % (dataset, dis, dataset, dis, type))
    return


if __name__ == '__main__':

    lst = []
    for i in os.listdir(dirs):
        lst.append(i.split('_')[0])

    # if 'GSE110999_ra' in lst:
    #     lst.remove('GSE110999_ra')
    #
    # if 'GSE110999_sle' in lst:
    #     lst.remove('GSE110999_sle')

    for i in lst:
        p = mp.Process(target=main, args=(dirs, i, meta))
        p.start()
        p.join()