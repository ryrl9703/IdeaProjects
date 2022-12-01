# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : tpm_copy.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/4 09:31
"""


import os

from utils import find_file


os.chdir('/public/workspace/ryrl/projects/rnaedit_autoimmune/data')



lst = []
for root, dirs, file in os.walk('./'):
    for i in dirs:
        if i == 'matrix':
            lst.append('%s/%s' % (root, i))


for i in lst:
    os.system('cp -r %s %s/%s' % (i,
                                  '/public/workspace/ryrl/projects/upload/database2/tmp/matrix', i.split('/')[-2]))