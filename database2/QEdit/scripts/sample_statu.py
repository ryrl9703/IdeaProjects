# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/5 11:00
# FileName: sample_statu
# Description:


import os
import numpy as np
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description= 'create sample status file for get_DE script')


parser.add_argument('--workdirectory', '-d',
                    dest='wd', metavar= 'work directory', required= True,
                    help= 'The directory that the script to work')

parser.add_argument('--meta', '-m',
                    dest= 'meta', metavar= 'file', default= 'matrix/metaInfo.txt',
                    help= 'file should contains sample name, disease, etc, defalut: matrix/metaInfo.txt')

parser.add_argument('--columns', '-c', nargs= 2,
                    dest= 'columns', metavar= 'columns', default= 'Run disease',
                    help= 'columns to extract from metaInfo file, default: Run disease')

parser.add_argument('--status', '-s',
                    dest= 'status', metavar= 'status', default= 'HC',
                    help= 'the name of the health sample, default: HC')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path', default= 'info/sample_status.txt',
                    help= 'where to save the final file, default: info/sample_status.txt')

# parser.add_argument('--type', '-t', nargs= 2,
#                     dest= 'type', metavar= 'disease status', required= True,
#                     help= 'status to describe the disease')

args = parser.parse_args()
wd = args.wd
# typ = args.type
meta = args.meta
out = args.output
status = args.status
col = args.columns.split(' ')



lst  = []

for i in os.listdir(wd):
    if i.startswith('GSE'):
        lst.append(i)  # TODO 为什么使用remove的时候会有些元素第一次无法删除

for i in lst:
    path = os.path.join(i, meta)
    outp = os.path.join(i, out)
    if os.path.exists(path):
        metaInfo = pd.read_csv(path, sep= '\t', header=0)
        try:
            if set(col).issubset(set(metaInfo.columns)):
                df = metaInfo[col]
                df['Type'] = df.iloc[:, 1]
                df = df.rename(columns= {df.columns[0]: 'Sample', df.columns[1]: 'Group'})
                # mask = df.Group == 'HC'  # TODO if not 'HC', is 'Healthly', how to solve it
                mask = df.Group == status
                df.Group[mask] = 'GROUPA'
                df.Group[mask == False] = 'GROUPB'
                df.to_csv(outp, sep=',', index=None)
            else:
                print('columns is not in metaInfo fiile')
        except ValueError:
            print('Error in line 55-60')
    else:
        print('%s not exit in %s' % (path, i))




