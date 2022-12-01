# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : deom.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/5 20:04
"""

import pymysql


conn = pymysql.connect(host='10.20.35.100',  # localhost
                       port=3306,
                       user='pcwang',
                       password='12280311',
                       database='mysql', charset='utf8')  # 需要mysql已经登录
csl = conn.cursor()
count = csl.execute('select component_id,component_group_id,component_urn from component')
print('results %s' % count)

for i in range(count):
    result = csl.fetchone()
    print(result)

csl.close()
conn.close()

