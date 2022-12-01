# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : merge_HC_PA_cis.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/2 15:22
"""


import os
import argparse
import pandas as pd


import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description= 'scripts to count the Alu Elements')

parser.add_argument('--directory', '-d',
                    dest='dirs',
                    metavar= 'directory',
                    type= str,
                    required= True,
                    help= 'The path to the directory that contains the cis-NATs intersect with edSites')

# parser.add_argument('--status', '-s',
#                     dest='status',
#                     metavar= 'status',
#                     type= str,
#                     required= True,
#                     choices=['HC', 'PA'],
#                     help= 'The status of the samples')


parser.add_argument('--output', '-o',
                    dest= 'output',
                    metavar= 'path',
                    required=True,
                    help= 'where to save the final file')

args = parser.parse_args()
dirs = args.dirs
opts = args.output


if __name__ == '__main__':

    df = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                     'database3/results/cis_NATs_related/cis_NATs_intersect_edSites/ByDataset/HC/GSE103489_HC.bed', sep='\t', header=None, low_memory=False)

    de = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                     'database3/results/cis_NATs_related/cis_NATs_intersect_edSites/ByDataset/PA/GSE103489_Patient.bed', sep='\t', header=None, low_memory=False)

































