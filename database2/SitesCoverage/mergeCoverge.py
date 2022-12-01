# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeCoverge.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/2 22:20
"""

import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/filter_5_1/ori')

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                       'data/metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)

lst = os.listdir('./')
for i in lst[:]:
    if i not in list(metaInfo.Run):
        lst.remove(i)

df = pd.read_csv('%s/%s.tsv' % (lst[0], lst[0]), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,4]]
df.rename(columns={'Coverage-q30': lst[0]})

for i in lst[1:]:

    de = pd.read_csv('%s/%s.tsv' % (i, i), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,4]]
    de = de.rename(columns={'Coverage-q30': i})

    df = pd.merge(df, de, on=['Region', 'Position', 'AllSubs'], how='outer')