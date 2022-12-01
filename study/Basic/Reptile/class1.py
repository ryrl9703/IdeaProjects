# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : class1.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/5 20:30
"""

"""
原理：通过编程，定向获取数据(图片、视频、文档、漫画、源码)

爬虫思路：三步
    1、访问服务器，获得权限，获取数据
    2、解析（防止乱码），筛选数据
    3、下载保存
"""

import requests
import re
print('初级'.center(100, '='))
num = 0
url = 'https://image.baidu.com/search/detail?ct=503316480&z=undefined&tn=baiduimagedetail&ipn=d&word=迪丽热巴&step_word=&ie=utf-8&in=&cl=2&lm=-1&st=undefined&hd=undefined&latest=undefined&copyright=undefined&cs=3257287698,842866553&os=3822847386,1885781660&simid=3330854307,362398698&pn=4&rn=1&di=46137345&ln=885&fr=&fmq=1667655404404_R&fm=&ic=undefined&s=undefined&se=&sme=&tab=0&width=undefined&height=undefined&face=undefined&is=0,0&istype=0&ist=&jit=&bdtype=11&spn=0&pi=0&gsm=1e&objurl=https%3A%2F%2Fgimg2.baidu.com%2Fimage_search%2Fsrc%3Dhttp%253A%252F%252Fwx2.sinaimg.cn%252Fmw690%252F006Je4bMgy1h7tdqemfulj30o016odqk.jpg%26refer%3Dhttp%253A%252F%252Fwx2.sinaimg.cn%26app%3D2002%26size%3Df9999%2C10000%26q%3Da80%26n%3D0%26g%3D0n%26fmt%3Dauto%3Fsec%3D1670247402%26t%3D393dc30f5ec7d05422aa51e43d1492f4&rpstart=0&rpnum=0&adpicid=0&nojc=undefined&dyTabStr=MCwzLDEsNCw1LDcsNiwyLDgsOQ%3D%3D'
res = requests.get(url).content

with open('./text.jpg') as f:
    f.write(res, 'ab')


print('高级'.center(100, '='))
header = ''

requests.get(url=url, headers=header).content.decode()  # 解析

# 筛选
a = re.findall(pattern='"objURL":"(.*?)"', string=res)

# 下载保存
for b in a:

    num += 1
    l = requests.get(b).content
    img = open('./%s.jpg' % b, 'ab')
    img.write(l)
    img.close()

