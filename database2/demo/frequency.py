# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : frequency.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/2 20:21
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/results/EditedGenes/final/filter5')

df = pd.read_csv('./edSites.tsv', sep='\t', header=0, low_memory=False)