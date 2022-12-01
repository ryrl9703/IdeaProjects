# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : siteCountsByDataset.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/14 14:13
"""

import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/')

metaInfo = pd.read_csv('data/metaInfo/metaInfo_IFNscore_HallMarkscores.txt', sep='\t', header=0)


sitesCounts = pd.read_csv('/public/workspace/ryrl/projects/upload/'
                          'database3/tmp/sitescounts.txt', sep='\t',header=0)

sitesCounts['Run'] = sitesCounts.Run.str.split('/', expand=True)[3]

sitesCounts.to_csv('/public/workspace/ryrl/projects/upload/'
                          'database3/tmp/sitescounts.txt', sep='\t', index=None)


# metaInfo.to_csv('./data/metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', index=None)