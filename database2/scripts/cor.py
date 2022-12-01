# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : cor.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/5 14:12
"""


import numpy as np
import pandas as pd
from scipy.stats import spearmanr


metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                       'data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0, low_memory=False)

array = np.array([])
for i in metaInfo.Dataset.drop_duplicates():
    df = metaInfo.loc[(metaInfo.Dataset == i) == True, :]
    array = np.append(array, i)
    array = np.append(array, spearmanr(df.ADAR, df.A2GEditingIndex))
    array = np.append(array, spearmanr(df.ADAR, df['IFN_score']))
    array = np.append(array, spearmanr(df.A2GEditingIndex, df['IFN_score']))

array = array.reshape(-1, 7)
array = pd.DataFrame(array)
array = array.rename(columns={array.columns[0]: 'dataset',
                              array.columns[1]: 'ADAR_a2g_cor',
                              array.columns[2]: 'pvalue',
                              array.columns[3]: 'ADAR_IFN',
                              array.columns[4]: 'pvalue_IFN',
                              array.columns[5]: 'a2g_IFN',
                              array.columns[6]: 'pvalue_a2g_IFN'})

array.to_csv('/public/workspace/ryrl/projects/'
             'upload/database3/results/Correlation/ADAR_IFN_A2G.txt', sep='\t', index=None)

