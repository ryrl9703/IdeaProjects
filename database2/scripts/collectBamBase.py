# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/5 14:27
# FileName: collectBamBase
# Description:


import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to collect the BAM bases')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory', required= True,
                    help= 'The path to the directory contain results')


parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
dirs = args.directory
output = args.output


def collectBamBase(directory:str):
    """

    :param directory:
    :return:
    """
    lst = []
    for i in os.listdir(directory):
        if i.endswith('base'):
            lst.append(i)

    df = pd.read_csv(os.path.join(directory, lst[0]), sep='\t', header=None)
    df = df.rename(columns={df.columns[0]: 'Base'})

    for i in lst[1:]:
        df1 = pd.read_csv(os.path.join(directory, i), sep='\t', header=None)
        df1 = df1.rename(columns={df1.columns[0]: 'Base'})
        df = pd.concat([df, df1], axis=0).reset_index(drop=True)

    df = pd.concat([df, pd.DataFrame(lst)], axis=1)
    df = df.rename(columns={df.columns[1]: 'Run'})
    df['Run'] = df.Run.str.split('.', expand=True)[0]
    return df


if __name__ == '__main__':
    df = collectBamBase(dirs)
    df.to_csv('%s.txt' % output, sep='\t', index=None)