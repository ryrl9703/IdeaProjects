# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : yeild.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/24 10:12
"""


def gen(n):
    for i in range(n):
        yield i

g = gen(5)