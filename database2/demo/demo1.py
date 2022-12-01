# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : demo.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/21 15:11
"""

import os
import pandas as pd
import multiprocessing as mp

def f(x, y):
    print(x, y)



if __name__ == '__main__':
    df = df
    at = df.iloc[:, 3:].apply(lambda x: x.str.split(',', expand=True)[0].str.replace(' ',''))
    gc = df.iloc[:, 3:].apply(lambda x: x.str.split(',', expand=True)[1].str.replace(' ',''))

    at.to_csv('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/split/BaseCount/AT.tsv', sep='\t', index=None)
    gc.to_csv('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/split/BaseCount/GC.tsv', sep='\t', index=None)

    pool = mp.Pool(5)
    for i in ['a', 'b', 'c', 'd']:
        pool.apply_async(f, (i,5))
    pool.close()
    pool.join()
