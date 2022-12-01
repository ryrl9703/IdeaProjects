# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : utils.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/27 10:17
"""

import os


def name(fname: str) -> str:
    return os.path.splitext(os.path.basename(fname))[0]

