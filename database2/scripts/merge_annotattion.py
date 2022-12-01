# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/1 19:09
# FileName: merge_annotattion
# Description:

import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge annotated sites')

parser.add_argument('--directory', '-d1', dest='directory',
                    metavar= 'directory', required= True,
                    help= 'The disease that the script to process, a directory')
parser.add_argument('--directory2', '-d2', dest='annovar',
                    metavar= 'annovar', required= True,
                    help= 'directory storer the annovar results')

# parser.add_argument('--site', '-s',
#                     dest='site', metavar='type',
#                     required= True, choices= ['redi', 'recoding'],
#                     help= 'The site type you want to process, choose from redi and recoding')

# parser.add_argument('--metaInfo', '-m',dest='metaInfo',
#                     metavar='sample information',required= True,
#                     choices= ['metaInfo', 'sample_status'],
#                     help= 'The file that contain sample information, choose from metaInfo and sample_status')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, help= 'where to save the final file')
args = parser.parse_args()
dir1 = args.directory
dir2 = args.annovar
output = args.output


for i in os.listdir(dir1):
    if i.endswith('snp151.txt'):
        df = pd.read_csv('%s/%s' % (dir1, i), sep='\t', header=0)
        df1 = pd.read_csv('%s/%s.hg38_multianno.txt' % (dir2, i.split('.')[0]),
                          sep='\t', header=0).drop(columns=['End','Alt'])
        df = pd.concat([df, df1], axis= 1).drop(columns=['Chr', 'Start', 'Ref'])
        df.to_csv('%s/%s' % (output, i), sep='\t', index=None)