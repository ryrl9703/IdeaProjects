# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : thread_based_paralleism.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/16 22:00
"""

import threading
from asyncio import start_server


def hello():
    print('hello, world')

def server():
    start_server()
    b.wait()
    while True:
        connection = make_connection()  # accept_connection()

if __name__ == '__main__':

    print('定时器对象'.center(100, '='))
    t = threading.Timer(30.0, hello)  # after 30 seconds, "hello, world" will be printed
    t.start()


    print('栅栏对象'.center(100, '='))