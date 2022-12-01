# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : Basic_information.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/20 14:09
"""

import os
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, ranksums

def get_datasets(metaInfo:pd.DataFrame) -> list:
    """

    :param metaInfo:
    :return:
    """

    return list(set(metaInfo.Dataset))

def get_files(dirs:str) -> list:
    """

    :param dirs:
    :return:
    """
    return os.listdir(dirs)

def sample_number(metaInfo:pd.DataFrame) -> pd.DataFrame:
    """

    :param metaInfo:
    :return:
    """
    datasets = get_datasets(metaInfo)

    df = pd.DataFrame(metaInfo[['Dataset', 'Disease_id', 'Sample_type']]).drop_duplicates(keep='first')
    arr = np.array([])
    for i in datasets:
        mask = metaInfo.Dataset == i
        de = metaInfo[mask].reset_index(drop=True)
        mask = de.Disease == 'HC'
        hc = de[mask].reset_index(drop=True).shape[0]
        arr = np.append(arr, (i, de.shape[0], hc, de.shape[0] - hc))

    arr = pd.DataFrame(arr.reshape(-1, 4), columns=['Dataset', '#Samples', '#Healthy', '#Patient'])
    df = pd.merge(df, arr, on=['Dataset'], how='inner')

    return df

def correlation(metaInfo:pd.DataFrame, col1:str, col2:str, df:pd.DataFrame) -> pd.DataFrame:
    """

    :param df:
    :param metaInfo: a data frame contains metaInfomation
    :param col1: one of the variable to correlate
    :param col2: the other of the variable to correlate
    :return:
    """

    datasets = get_datasets(metaInfo)
    array = np.array([])

    for i in datasets:
        mask = metaInfo.Dataset == i
        de = metaInfo[mask].reset_index(drop=True)
        array = np.append(array, (i,
                                  spearmanr(de[col1], de[col2])[0], spearmanr(de[col1], de[col2])[1]))
    array = pd.DataFrame(array.reshape(-1, 3))
    array = array.rename(columns={array.columns[0]: 'Dataset',
                                  array.columns[1]: 'cor_%s_%s' % (col1, col2),
                                  array.columns[2]: 'pvalue_%s_%s' % (col1, col2)})
    df = pd.merge(df, array, on=['Dataset'], how='inner')

    return df

def get_pvalue(metaInfo:pd.DataFrame, col:str, df:pd.DataFrame) -> pd.Series:
    """

    :param df:
    :param metaInfo:
    :param col:
    :return:
    """

    datasets = get_datasets(metaInfo)
    array = np.array([])

    for i in datasets:
        mask = metaInfo.Dataset == i
        de = metaInfo[mask].reset_index(drop=True)
        s, p = ranksums(de[de.Disease == 'HC'][col].dropna(), de[de.Disease != 'HC'][col].dropna())
        array = np.append(array, (i, p))
    else:
        array = pd.DataFrame(array.reshape(-1, 2))
        array = array.rename(columns={array.columns[0]: 'Dataset',
                                      array.columns[1]: 'pvalue_%s' % col})

        df = pd.merge(df, array, on=['Dataset'], how='inner')

    return df



def count_sites(dirs:str, df:pd.DataFrame, status:str='PA') -> pd.DataFrame:
    """

    :param status:
    :param df:
    :param dirs:
    :return:
    """

    lst = get_files(dirs)

    array = np.array([])
    for i in lst:
        s = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0, low_memory=False)
        array = np.append(array, (i.split('.')[0], s.shape[0]))
    array = pd.DataFrame(array.reshape(-1, 2), columns=['Dataset', '#%s_%s' % (dirs.split('/')[-3], status)])
    df = pd.merge(df, array, on=['Dataset'], how='left')

    return df

def count_region(dirs:str, df:pd.DataFrame) -> pd.DataFrame:
    """

    :param dirs:
    :param df:
    :return:
    """

    lst = get_files(dirs)

    t = pd.DataFrame()
    r = pd.DataFrame()
    for i in lst:

        s = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0, low_memory=False)
        s.rmsk_tid = s.rmsk_tid.apply(lambda x: x if x == '-' else x.split('-')[0])
        s.rmsk_tid = s.rmsk_tid.apply(lambda x: x if x == 'Alu' or x == 'L1' else 'Other')

        r = pd.concat([r, pd.DataFrame(s.rmsk_tid.value_counts())], axis=1)
        r = r.rename(columns={'rmsk_tid': i.split('_')[0]})

        t = pd.concat([t, pd.DataFrame(s.Func_refGene.value_counts())], axis=1)
        t = t.rename(columns={'Func_refGene': i.split('_')[0]})


    df = pd.merge(df, r.T, left_on=['Dataset'], right_index=True, how='left')
    df = pd.merge(df, t.T, left_on=['Dataset'], right_index=True, how='left')

    return df




def main():

    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/data/'
                           'metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)
    mask = metaInfo.Disease != 'HC'
    metaInfo.iloc[metaInfo[mask].Disease.index, 3] = 'Patient'

    df = sample_number(metaInfo)
    df = correlation(metaInfo, 'ADAR', 'A2GEditingIndex', df)
    df = correlation(metaInfo, 'IFN_score', 'A2GEditingIndex',df)
    df = get_pvalue(metaInfo, 'ADAR', df)
    df = get_pvalue(metaInfo, 'A2GEditingIndex', df)
    df = count_sites('/public/workspace/ryrl/projects/upload/database3/results/RegulationSites/PA/FDR', df)
    df = count_sites('/public/workspace/ryrl/projects/upload/database3/results/Sites/Recoding/DataSets/PA', df)
    # df = count_sites('/public/workspace/ryrl/projects/upload/database3/results/Sites/Recoding/DataSets/HC', df, 'HC')
    df = count_region('/public/workspace/ryrl/projects/upload/database3/results/Sites/DataSet/PA/remove_chrXYM', df)
    # df = count_region('/public/workspace/ryrl/projects/upload/database3/results/Sites/DataSet/HC/remove_chrXYM', df, 'HC')

    return df



if __name__ == '__main__':

    # col1 = 'ADAR'
    # col2 = 'A2GEditingIndex'

    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/RegulationGenes/PA/FDR'
    # dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/DataSet/PA/remove_chrXYM'
    # i = 'GSE103489_Patient.tsv'

    df = main()
    df.to_csv('/public/workspace/ryrl/projects/upload/database3/results/'
              'Statistics/ByDatasets/basicInformation/Basic_information.tsv', sep='\t', index=False)
