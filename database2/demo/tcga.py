# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : tcga.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/21 13:13
"""


import os
import pandas as pd


os.chdir('/public/workspace/ryrl/projects/tcga/immuneCellsProportion/TCGA')

lst = os.listdir('./')

df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
df['type'] = lst[0].split('.')[1]

for i in lst[1:]:
    df1 = pd.read_csv(i, sep='\t', header=0, low_memory=False)
    df1['type'] = i.split('.')[1]
    df = pd.concat([df, df1], axis=0)

df['Sample'] = df.index + '-01'

df = df.loc[:, ['Sample', 'type']]
df.to_csv('../metaInfo.txt', sep='\t', index=None)