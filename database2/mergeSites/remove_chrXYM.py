# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : remove_chrXYM.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/21 20:41
"""


import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to remove the sites in chrX, chrY, chrM')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the annotated editing Sites')

parser.add_argument('--column', '-c',
                    dest='col',
                    metavar= 'column',
                    type= str,
                    default= 'Region',
                    help= 'The column used to filter, default: Region')

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
                    help= 'where to save the filtered file')

args = parser.parse_args()
dirs = args.dirs
cols = args.col
thrd = args.thread
opts = args.output


def remove_chrXYM(dirs:str, file:str, col:str) -> pd.DataFrame:
    """

    :param col:
    :param dirs:
    :param file:
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=0, low_memory=False)
    mask = df[col].str.contains(r'(X|Y|M)$')
    df = df[mask == False].reset_index(drop=True)

    df.to_csv('%s/%s' % (opts, file), sep='\t', index=False)

    return None

if __name__ == '__main__':

    lst = os.listdir(dirs)
    pool = mp.Pool(thrd)
    for i in lst:
        pool.apply_async(remove_chrXYM, args=[dirs, i, cols])
    pool.close()
    pool.join()