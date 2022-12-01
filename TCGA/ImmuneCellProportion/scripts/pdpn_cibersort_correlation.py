# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : pdpn_cibersort_correlation.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/27 10:45
"""


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import spearmanr


def correlation_celltype(df:pd.DataFrame, cancer:str, celltype:str):
    """

    :param df: a dataframe contains pdpn TPM and the cell proportion
    :param cancer: caner type
    :param celltype: celltype
    :return:
    """

    mask = df.project == cancer
    pdpn = df[mask].pdpn
    cibersort = df[mask].loc[:, celltype]
    cor, p = spearmanr(pdpn, cibersort)

    return cor, p


if __name__ == '__main__':

    df = pd.read_csv('./ImmuneCellProportion/data/cibersort_T_macrophage.tsv', sep='\t', header=0, low_memory=False)
    df = df.rename(columns={'tpm_unstranded': 'pdpn'})

    cancerType = df.project.drop_duplicates().reset_index(drop=True).to_list()
    cellType = df.columns[5:].to_list()

    correlation = []
    pvalue = []
    for i in cancerType:
        for j in cellType:
            cor, p = correlation_celltype(df, i, j)

            correlation.append(cor)
            pvalue.append(p)

    correlation = pd.DataFrame(np.array(correlation).reshape(32, -1))
    correlation.columns = cellType
    correlation.index = cancerType

    correlation.to_csv('%s/%s' % ('./ImmuneCellProportion/results/', 'cor_matrix.tsv'), sep='\t', index=True)

    pvalue = pd.DataFrame(np.array(pvalue).reshape(32, -1))
    pvalue.columns = cellType
    pvalue.index = cancerType

    pvalue.to_csv('%s/%s' % ('./ImmuneCellProportion/results/', 'pvalue_matrix.tsv'), sep='\t', index=True)


    sns.heatmap(correlation)
    plt.show()

    print('test'.center(100, '='))

    for i in cancerType:
        cor, p = df.iloc[:, 5:].apply(correlation_celltype, axis=1, args=[i])