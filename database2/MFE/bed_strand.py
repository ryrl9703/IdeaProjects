# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : bed_strand.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/17 10:24
"""


import os
import argparse
import pandas as pd
import multiprocessing as mp

parser = argparse.ArgumentParser(description= 'scripts to correcte the strand')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'work directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains annotated edSites files')

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

parser.add_argument('--output2', '-o2',
                    dest= 'output2',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the bed region file, which use to get fasta sequence')

args = parser.parse_args()
dirs = args.dirs
thrd = args.thread
opts = args.output
opt2 = args.output2

def strand(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """

    df = pd.read_csv('%s/%s' % (dirs, file), sep='\t', header=0, low_memory=False)
    mask = df['Region'].str.contains(r'(X|Y|M)$')
    df = df[mask == False].reset_index(drop=True)

    df['Strand'] = df['Strand'].astype(str).str.replace('0', '-')
    df['Strand'] = df['Strand'].astype(str).str.replace('2', '+/-')
    df['Strand'] = df['Strand'].astype(str).str.replace('1', '+')

    df.to_csv('%s/%s' % (opts, file), sep='\t', index=False)

    return None

def bed_region(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """
    df = pd.read_csv('%s/%s' % (opts, file), sep='\t', header=0, low_memory=False)
    df = df.drop(columns=df.columns[9:14])
    col_name = df.columns.tolist()
    col_name.insert(col_name.index('Position') + 1, 'End')
    df = df.reindex(columns=col_name)
    df['End'] = df['Position'] + 50
    df['Position'] = df['Position'] - 51


    df = pd.concat([df.iloc[:, 0:5], df.iloc[:, [11, 19]]], axis=1)

    df.to_csv('%s/%s.bed' % (opt2, file.split('.')[0]), sep='\t', header=False, index=False)

    return None


if __name__ == '__main__':

    # os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/ori')
    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/ori'
    #
    # file = lst[0]
    # opts = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/remove_chrxym_correct_strand'
    # opt2 = '/public/workspace/ryrl/projects/upload/database3/results/Sites/MFE/Bed'

    lst = os.listdir(dirs)

    if not os.path.exists('%s/%s' % (opts, lst[-1])):
        pool = mp.Pool(thrd)
        for i in lst:
            pool.apply_async(strand, args=(i,))
        pool.close()
        pool.join()
    else:
        print('Files have been remove chrX,chrY,chrM')


    if not os.path.exists('%s/%s.bed' % (opt2, lst[-1].split('.')[0])):
        pool = mp.Pool(thrd)
        for i in lst:
            pool.apply_async(bed_region, args=(i,))
        pool.close()
        pool.join()
    else:
        print('Bed region files have exited!')