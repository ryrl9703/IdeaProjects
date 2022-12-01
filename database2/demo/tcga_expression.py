# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : tcga_expression.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/22 14:52
"""

import os
import pandas as pd

def getpdpnTpm(file:str) -> pd.DataFrame:
    """

    :param file:
    :return:
    """

    df = pd.read_csv(file, sep='\t', header=0, skiprows=[0,2,3,4,5])
    mask = df.gene_name == 'PDPN'
    df = df[mask].iloc[:, [0,1,2,6]]
    df.index = [file.split('/')[-2]]
    return df

def concatpdpnTpm(dirs:str) -> pd.DataFrame:
    """

    :param dirs:
    :return:
    """

    lst = []
    for root, dirs, files in os.walk('./dataDownload'):
        for i in files:
            lst.append('%s/%s' % (root, i))

    df = getpdpnTpm(lst[0])
    for i in lst[1:]:
        df1 = getpdpnTpm(i)
        df = pd.concat([df, df1], axis=0)
    return df



if __name__ == '__main__':


    df = concatpdpnTpm('./dataDownload')
    df.to_csv('./files/pdpnTPM.tsv', sep='\t', index=True)
#     os.chdir('/public/workspace/ryrl/projects/tcga/immuneCellsProportion')
#
#     df = pd.DataFrame()
#     lst = []
#     for root, dirs, files in os.walk('./dataDownload'):
#         for i in files:
#             lst.append('%s/%s' % (root, i))
#             # df1 = pd.read_csv('%s/%s' % (root, i), sep='\t', skiprows=[0,2,3,4,5])
#
#     df = pd.read_csv(lst[0], sep='\t', header=0, skiprows=[0,2,3,4,5])
#     mask = df.gene_name == 'PDPN'
#     df = df[mask].iloc[:, [0, 1, 2, 6]]
