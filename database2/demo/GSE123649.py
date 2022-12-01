# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : GSE123649.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/4 21:40
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database2/tmp/tpm/matrix/GSE123649/count')

lst = os.listdir('.')

df = pd.read_csv('./%s' % lst[0], sep='\t', header=0)

for i in lst[1:]:
    df1 = pd.read_csv('./%s' % i, sep='\t', header=0)
    df = pd.merge(df, df1, on=['ENSEMBL_GENEID'], how='outer')

df.to_csv('../GSE123649_tpm.txt', sep='\t', index=None)

