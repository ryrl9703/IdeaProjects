# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/5 21:44
# FileName: Introduction
# Description:


from multiprocessing import Pool, Process

def f(x):
    return x * x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()

import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('fork')
    # mp.get_context('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()


print('Exchanging objects between processes'.center(100, '='))

# Queues: The Queues class is a near clone of queue.Queue.
import multiprocessing as mp
def q():
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = mp.Queue
    p = mp.Process(target=q, args=(q,))
    p.start()
    print(q.get())  # print "[42,None,'hello]"
    p.join()