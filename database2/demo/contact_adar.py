# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : contact_adar.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/5 08:48
"""

import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database2/expression/ADAR')

lst = os.listdir('.')

df = pd.read_csv('%s' % lst[0], sep='\t', header=0, index_col=0)

for i in lst[1:]:
    df1 = pd.read_csv('%s' % i, sep='\t', header=0, index_col=0)
    df = pd.concat([df, df1], axis=0)

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/'
                       'upload/database2/metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0)

pd.DataFrame(metaInfo.columns)
metaInfo = pd.merge(metaInfo.iloc[:, 0:19], df,
                    left_on=['sample_name'], right_index=True, how='left')


lst = os.listdir('../GSVA_score')

df = pd.read_csv('%s/%s' % ('../GSVA_score', lst[0]), sep='\t', header=0, index_col=0)

for i in lst[1:]:
    df1 = pd.read_csv('%s/%s' % ('../GSVA_score', i), sep='\t', header=0, index_col=0)
    df = pd.concat([df, df1], axis=0)

metaInfo = pd.merge(metaInfo, df, on=['sample_name'], how='left')

metaInfo.to_csv('/public/workspace/ryrl/projects/upload/'
                'database2/metaInfo/metaInfo_HallMarkScore.txt', sep='\t', index=None)