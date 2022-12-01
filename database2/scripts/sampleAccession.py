# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : sampleAccession.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/24 12:48
"""

import sys

import pandas as pd

sys.path.append("..")
from utils import find_file

# os.chdir('/public/workspace/ryrl/projects/rnaedit_autoimmune/data')

# lst = find_file('/public/workspace/ryrl/projects/rnaedit_autoimmune/data', 'SRR_Acc_List.txt')
metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/finalResults/metaInfo/metaInfo_add_ISG.txt',
                       sep='\t', header=0, low_memory=False)

samples = pd.read_csv('/public/workspace/ryrl/projects/upload/database2/download/REDIportal.csv',
                      sep=',', header=0, low_memory=False)

df = pd.merge(metaInfo.iloc[:, 0], samples.iloc[:, [0, 1]], left_on='Run', right_on='Sample')
