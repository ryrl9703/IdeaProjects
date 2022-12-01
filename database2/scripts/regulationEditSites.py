# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/12 10:37
# FileName: regulationEditSites
# Description:


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset')

dirs = 'Psoriasis'
lst = []
for i in os.listdir(dirs):
    lst.append(i.split('.')[0].split('_')[0])
    lst = list(set(lst))


for i in lst:
    genes = pd.read_csv('%s/%s_toAnno.txt.variant_function' % (dirs,i), sep='\t', header=None)
    genes['genes'] = genes.iloc[:, 1].str.split('(', expand=True)[0]
    sites = pd.read_csv('%s/%s.txt' % (dirs,i), sep='\t', header=0)
    df = pd.concat([sites.iloc[:, 0:6], genes.iloc[:, [0,1,7]], sites.iloc[:, 6:]], axis=1)
    df['genes'] = df['genes'].str.split(',')
    df = df.explode('genes')
    df.to_csv('%s/%s.contact.txt' % (dirs, i), sep='\t', index=None)