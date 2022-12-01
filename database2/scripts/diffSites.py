# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : diffSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/13 20:17
"""


import os
import sys
import pandas as pd
sys.path.append('/public/workspace/ryrl/idea/database2')
from utils import splitserise

# os.chdir('/public/workspace/ryrl/projects/rnaedit_autoimmune/data')
#
# lst = find_file('./', 'de_sites.txt')
#
#
# for i in lst:
#     os.system("cp %s '/public/workspace/ryrl/projects/upload/"
#               "database2/diffSites/ori/%s_diffSites.txt'" % (i, i.split('/')[-5]))
#
# os.chdir('/public/workspace/ryrl/projects/upload/database2/diffSites/ori')
# lst = os.listdir('./')

# df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
# # df.significant.value_counts()
#
# s = df.iloc[:, 3:len(df.columns)-5].apply(splitserise, axis=0)
# pd.concat([df.iloc[:, 0:3], s, df.iloc[:, len(df.columns)-5:len(df.columns)-1]], axis=1)

if __name__ == '__main__':
    os.chdir('/public/workspace/ryrl/projects/upload/database2/diffSites')
    lst = os.listdir('./ori')

    for i in lst:
        df = pd.read_csv('ori/%s' % i, sep='\t', header=0, low_memory=False)
        s = df.iloc[:, 3:len(df.columns) - 5].apply(splitserise, axis=1)
        df = pd.concat([df.iloc[:, 0:3], s, df.iloc[:, len(df.columns) - 5:len(df.columns)]], axis=1)
        df.to_csv('frequency/%s' % i, sep='\t', index=None)

    print('split significant diffSites'.center(100, '='))
    lst = os.listdir('./frequency')

    for i in lst:
        df = pd.read_csv('frequency/%s' % i, sep='\t', header=0, low_memory=False)
        mask = df.significant == 'yes'
        df = df[mask == True]
        df.to_csv('significant/%s' % i, sep='\t', index=None)

    print('prepare sites to annotation'.center(100, '='))
    lst = os.listdir('annotation/ori')

    for i in lst:
        df = pd.read_csv('annotation/ori/%s' % i, sep='\t', header=0, low_memory=False)
        if len(df.index) >= 1:
            df.editing_type = df.editing_type.str.split('', expand=True)[1]
            df = df.rename(columns={'chromosome': 'Region', 'position': 'Position', 'editing_type': 'Reference'})
            df.to_csv('annotation/sites/%s' % i, sep='\t', index=None)

    print('Contact annotation and frequency'.center(100, '='))
    lst = os.listdir('annotation/snp151')
    for i in lst:
        fre = pd.read_csv('significant/%s' % i, sep='\t', header=0, low_memory=False)
        df = pd.read_csv('annotation/snp151/%s' % i, sep='\t', header=0, low_memory=False)
        df = pd.concat([df, fre], axis=1)
        df.to_csv('annotation/results/%s' % i, sep='\t', index=None)


    print('Merge frequency by sample'.center(100, '='))
    lst = os.listdir('annotation/results')

    df = pd.read_csv('annotation/results/%s' % lst[0], sep='\t', header=0, low_memory=False)
    df = df.drop(columns=['Region', 'Position', 'Reference', 'refGene_feat',
                          'rmsk_feat', 'rmsk_gid', 'rmsk_tid', 'snp151_feat', 'snp151_gid', 'snp151_tid'])
    for i in lst[1:]:
        df1 = pd.read_csv('annotation/results/%s' % i, sep='\t', header=0, low_memory=False)
        df1 = df1.drop(columns=['Region', 'Position', 'Reference', 'refGene_feat',
                                'rmsk_feat', 'rmsk_gid', 'rmsk_tid', 'snp151_feat', 'snp151_gid', 'snp151_tid'])
        df = pd.merge(df, df1, on=['chromosome', 'position', 'editing_type', 'refGene_gid'], how='outer')

    df.to_csv('annotation/mergediffSites.txt')

    df = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/diffSites/adjust/GSE89408_diffSites.txt', sep='\t', header=0, low_memory=False)
    df.cat.value_counts()

    print('FDR sig'.center(100, "="))
    lst = os.listdir('adjust')

    for i in lst:
        df = pd.read_csv('adjust/%s' % i, sep='\t', header=0, low_memory=False)
        mask = df.cat == 'sig'
        df = df[mask == True]
        df.to_csv('significant/FDR/%s' % i, sep='\t', index=None)
