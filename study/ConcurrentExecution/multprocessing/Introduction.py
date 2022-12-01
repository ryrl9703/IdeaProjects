# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : Introduction.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/14 20:13
"""

from multiprocessing import Pool, Process
import os
import sys
sys.path.append('/public/workspace/ryrl/idea/study/multprocessing')

from utils import f,f1,info

import multiprocessing as mp

from multiprocessing import Process, Queue, Pipe, Lock



def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

def foo(q):
    q.put('Hello')


def f(q):
    q.put([42, None, 'hello'])



with Pool(5) as p:
    print(p.map(f, [1, 2, 3]))


p = Process(target=f1, args=('bob',))
p.start()
p.join()

info('main line')
p = Process(target=f, args=('bob',))
p.start()
p.join()

mp.set_start_method('spawn')
q = mp.Queue
p = mp.Process(target=foo, args=(q,))
p.start()
print(q.get())
p.join()

print('在进程之间交换对象'.center(100, '='))
print('队列'.center(100, '-'))
q = Queue()
p = Process(target=f, args=(q,))
p.start()
print(q.get())  # prints "[42, None, 'hello']"
p.join()

print('Pipe'.center(100, '-'))

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

parent_conn, child_conn = Pipe()
p = Process(target=f, args=(child_conn,))
p.start()
print(parent_conn.recv())
p.join()

print('进程间同步'.center(100, '='))
def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

lock = Lock()
for num in range(10):
    Process(target=f, args=(lock, num)).start()

print('进程键共享状态'.center(100, '='))
"""
multiprocessing提供了两种共享数据的方法：共享内存、服务进程
"""
print('共享内存'.center(100, '-'))
from multiprocessing import Process, Value, Array
def f(n, a):
    n.value = 3.1415907
    for i in range(len(a)):
        a[i] = -a[i]

num = Value('d', 0.0)
arr = Array('i', range(10))

p = Process(target=f, args=(num, arr))
p.start()
p.join()

print(num.value)
print(arr[:])

print('服务进程'.center(100, '-'))
# 由Manger()返回的管理对象控制一个服务进程， 该进程保存python对象并允许其他进程使用代理操作它们。
# Manger()返回的管理器支持类型：list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore,
# Condition, Event, Barrier, Queue, Value, Array
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

with Manager() as manager:
    d = manager.dict()
    l = manager.list(range(10))

    p = Process(target=f, args=(d, l))
    p.start()
    p.join()
    print(d)
    print(l)

print('使用工作进程'.center(100, '-'))
# Pool 类表示一个工作进程池。它具体有允许以几种不同方式将任务分配到工作进程的方法
from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x * x

with Pool(processes=4) as pool:

    # print "[0,1,4,...,81]"
    print(pool.map(f, range(10)))

    # print same numbers in arbitrary order
    for i in pool.imap_unordered(f, range(10)):
        print(i)

    # evaluate "f(20)" asynchronously
    res = pool.apply_async(f, (20,))  # run in only one process
    print(res.get(timeout=1))  # print  400

    # evaluate "os.getpid()" asynchronously
    res = pool.apply(os.getpid(), ())  # run in only one process
    print(res.get(timeout=1))

    # launching multiple evaluations asynchronously may use more processes
    multiple_results = [pool.apply_async(os.getpid(), ()) for i in range(4)]
    print([res.get(timeout=1) for res in multiple_results])

    # make a single worker sleep for 10 secs
    res = pool.apply_async(time.sleep(), (10,))
    try:
        print(res.get(timeout=1))
    except TimeoutError:
        print('We lacked patients and got a multiprocessing.TimeoutError')

    print('For the moment, the pool remains available for more work')

# exiting the 'with'-block has stopped the pool
print('Now the pool is closed and no longer available')
