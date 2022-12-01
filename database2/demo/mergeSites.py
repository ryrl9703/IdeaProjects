# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/6 12:03
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database2/frequency')

lst = os.listdir('./')

df= pd.read_csv(lst[0], sep='\t', header=0).iloc[:, 0:2]

for i in lst:
    df1 = pd.read_csv(i, sep='\t', header=0).drop(columns=['AllSubs', 'Func_refGene', 'Gene_refGene'])

    df = pd.merge(df, df1, how='inner', on=['Region', 'Position'])