# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : spearmanEditingLevel.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/16 13:44
"""


import os
import pandas as pd
import numpy as np
from scipy import stats

# os.chdir('/public/workspace/ryrl/projects/upload/database3/data/metaInfo')

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                       'data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0, low_memory=False)

dataset = set(metaInfo.Dataset)

for i in dataset:
    mask = metaInfo.Dataset == i
    d = metaInfo[mask]
    mask = d.Disease == 'HC'
    h = d[mask].A2GEditingIndex.reset_index(drop=True)
    h.name = 'Healthy'
    p = d[mask == False].A2GEditingIndex.reset_index(drop=True)
    p.name = 'Patient'

    df = pd.concat([h, p], axis=1)
    stats.wilcoxon(df.Healthy, df.Patient)