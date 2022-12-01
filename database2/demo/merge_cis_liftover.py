# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : merge_cis_liftover.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/4 19:30
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/data/cis_NATs/concat/filtered2')

cis = pd.read_csv('./cis_NATs.tsv', sep='\t', header=None, low_memory=False)

ori = pd.read_csv('./cis_filtered60_100000.tsv', sep='\t', header=0, low_memory=False)

cis = pd.merge(cis, ori.iloc[:, 3:], left_on=[cis.columns[3]], right_on=['cisNAT_ID'], how='left')
cis = cis.drop(columns=cis.columns[3])
cis = cis.rename(columns={cis.columns[0]: 'Chr', cis.columns[1]: 'start', cis.columns[2]: 'end'})

cis.to_csv('./cis_NATs_hg38.tsv', sep='\t', index=None)


os.chdir('/public/workspace/ryrl/projects/upload/database3/results/cis_NATs_related/cis_NATs_intersect_edSites/ByDisease/HC/filtered2/cis_NATs_edSites')

lst = os.listdir('./')

for i in lst:
    df = pd.read_csv(i, sep='\t', header=None, low_memory=False)
    cis_genes = df.drop_duplicates(subset=[df.columns[0], df.columns[1], df.columns[2], df.columns[3]])
    cis_genes.to_csv('../cis_NATs_unique/%s' % i, sep='\t', index=None)