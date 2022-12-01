# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : demo3.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/18 09:59
"""

import os
import pandas as pd

def mergeSites(lst:list, dirs:str) -> pd.DataFrame:
    """

    :param dirs:
    :param lst:
    :return:
    """
    df = pd.read_csv('%s/%s.txt' % (dirs, lst[0]), sep='\t', header=0, low_memory=False).iloc[:, [0,1,2,8]]
    df = df.rename(columns={'Frequency': lst[0]})

    for i in lst[1:]:
        de = pd.read_csv('%s/%s.txt' % (dirs, i), sep='\t', header=0, low_memory=False).iloc[:, [0,1,2,8]]
        de = de.rename(columns={'Frequency': i})
        df = pd.merge(df, de, on=['Region', 'Position', 'Reference'], how='outer')

    return df


if __name__ == '__main__':

    # os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/remove_chrxym_correct_strand')
    dirs = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Samples/remove_chrxym_correct_strand'



    metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/data/'
                           'metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)
    mask = metaInfo.Dataset == 'GSE89408'
    metaInfo = metaInfo[mask]
    metaInfo.Phenotype.value_counts()

    mask = metaInfo.Phenotype == '-'
    lst1 = list(metaInfo[mask].Run)

    mask = metaInfo.Phenotype == 'Rheumatoid arthritis (early)'
    lst2 = list(metaInfo[mask].Run)

    mask = metaInfo.Phenotype == 'Rheumatoid arthritis (established)'
    lst3 = list(metaInfo[mask].Run)

    hc = mergeSites(lst1, dirs)

    early = mergeSites(lst2, dirs)

    established = mergeSites(lst3, dirs)

    df1 = pd.merge(hc.iloc[:, 0:3], early.iloc[:, 0:3], on=['Region', 'Position', 'Reference'], how='inner')

    hc_ = pd.concat([hc.iloc[:, 0:3], early.iloc[:, 0:3], early.iloc[:, 0:3]]).drop_duplicates(keep=False)

    hc.iloc[hc_.index, :]