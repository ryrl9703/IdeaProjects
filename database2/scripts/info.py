# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : info.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/17 12:23
"""


import os
import sys
sys.path.append('/public/workspace/ryrl/idea/database2')
import pandas as pd
from utils import find_file

print('SRR_Acc_List'.center(100, '='))
os.chdir('/public/workspace/ryrl/projects/rnaedit_autoimmune/data')

lst = find_file('./', 'sample_status.txt')

for i in lst:
    os.system("cp %s '/public/workspace/ryrl/projects/upload/database2/rediTable/info/sample_status/%s.txt'" % (i, i.split('/')[-3]))

