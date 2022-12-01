# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : SitesMergeByDisease.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/16 22:55
"""

import os
import pandas as pd

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                       'data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)

disease = set(metaInfo.Disease_id)

for i in disease:
    mask = metaInfo.Disease_id == i
    lst = list(set(metaInfo[mask].Dataset))

    cols = ['Region', 'Position', 'AllSubs']
    df = pd.read_csv('%s/%s.tsv' % ('/public/workspace/ryrl/projects/upload/database2/'
                                'rediTable/filtered/mergeSitesByDataset/only_sites/sites', lst[0]), sep='\t', header=0)[cols]

    for s in lst[1:]:
        df1 = pd.read_csv('%s/%s.tsv' % ('/public/workspace/ryrl/projects/upload/database2/'
                                'rediTable/filtered/mergeSitesByDataset/only_sites/sites', s), sep='\t', header=0)[cols]

        df = pd.merge(df, df1, on=cols, how='outer')
    df.to_csv('%s/%s.tsv' % ('/public/workspace/ryrl/projects/upload/database2/'
                         'rediTable/filtered/mergeSitesByDisease', i), sep='\t', index=None)