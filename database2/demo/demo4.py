# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : demo4.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/22 20:18
"""


import numpy as np
import pandas as pd

array = np.array([['小三班', '周圣楷', '男','320722201812310154', '-', '学生','苏州市 木渎镇 和雍锦园 11栋403'],
                  ['-', '周李伟', '男', '320722198707094213', '-', '爸爸','居住地址 苏州市 木渎镇 和雍锦园 11栋403'],
                  ['-', '杨周', '女','320722198806067800', '-', '妈妈','苏州市 木渎镇 和雍锦园 11栋403'],
                  ['-', '李贞美', '女', '372833196507150328', '-', '奶奶', '苏州市 木渎镇 和雍锦园 11栋403']])

df = pd.DataFrame(array, columns=['班级', '姓名', '性别', '身份证号', '联系方式', ])