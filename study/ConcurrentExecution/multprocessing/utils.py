# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : utils.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/14 20:38
"""
import os


def f(x):
    return x * x



def f1(name):
    print('hello', name)


def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())