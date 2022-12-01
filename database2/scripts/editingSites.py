# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : editingSites.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/14 12:03
"""

import os

import numpy as np
import pandas as pd

if __name__ == '__main__':
    os.chdir('/public/workspace/ryrl/projects/upload/database2')

    metaInfo = pd.read_csv('./metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0, low_memory=False)
    # metaInfo.shape
    # metaInfo.columns
    # metaInfo.disease.value_counts()

    srr = list(metaInfo[(metaInfo.disease == 'HC') == True].Run)

    sites = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (srr[0], srr[0]),
                        sep='\t', header=0, low_memory=False).iloc[:, 0:3]
    for i in srr[1:]:
        if os.path.exists('./rediTable/ori/%s/%s.tsv' % (i, i)):
            df = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (i, i), sep='\t', header=0, low_memory=False).iloc[:, 0:3]
            sites = pd.merge(sites, df, how='outer', on=['Region', 'Position', 'Reference'])
        else:
            print('%s not exit' % i)  # SRR15372438

    sites.to_csv('./figures/2022_09_14/sites_HC_patients/HealthySites.txt', sep='\t', index=None)

    patient = list(metaInfo[(metaInfo.disease != 'HC') == True].Run)
    sites = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (patient[0], patient[0]),
                        sep='\t', header=0, low_memory=False).iloc[:, 0:3]

    for i in patient[1:]:
        if os.path.exists('./rediTable/ori/%s/%s.tsv' % (i, i)):
            df = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (i, i), sep='\t', header=0, low_memory=False).iloc[:, 0:3]
            sites = pd.merge(sites, df, how='outer', on=['Region', 'Position', 'Reference'])
        else:
            print('%s not exit' % i)

    sites.to_csv('./figures/2022_09_14/sites_HC_patients/PatientSites.txt', sep='\t', index=None)

    print('each dataset sites HC, Patient'.center(10, '='))

    datasets = list(metaInfo.dataset.drop_duplicates())
    d = 'HC'
    for i in datasets:
        s = metaInfo[metaInfo.dataset == i]
        srr = list(s[(s.disease != d) == True].Run)
        if 'SRR15372438' in srr:
            srr.remove('SRR15372438')

        if srr:
            sites = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (srr[0], srr[0]),
                                sep='\t', header=0, low_memory=False).iloc[:, 0:3]

            for j in srr[1:]:
                if os.path.exists('./rediTable/ori/%s/%s.tsv' % (j, j)):
                    df = pd.read_csv('./rediTable/ori/%s/%s.tsv' % (j, j),
                                     sep='\t', header=0, low_memory=False).iloc[:, 0:3]
                    sites = pd.merge(sites, df, how='outer', on=['Region', 'Position', 'Reference'])
                else:
                    print('%s not exit' % j)
            sites.to_csv('./figures/2022_09_14/sites_HC_patients/datasets/%s_Patient.txt' % i, sep='\t', index=None)
        else:
            print('%s have no %s samples' % (i, d))

    print('Statistic'.center(100, '='))
    metaInfo = pd.read_csv('./metaInfo/metaInfo_add_ISG.txt', sep='\t', header=0, low_memory=False)
    datasets = list(metaInfo.dataset.drop_duplicates())

    a = np.array([])
    for i in datasets:
        df = pd.read_csv('figures/2022_09_14/sites_HC_patients/'
                         'datasets/%s_Healthy.txt' % i, sep='\t', header=0, low_memory=False)

        df1 = pd.read_csv('figures/2022_09_14/sites_HC_patients/'
                          'datasets/%s_Patient.txt' % i, sep='\t', header=0, low_memory=False)

        s = df.Region.str.cat(df.Position.astype(str), sep='_').str.cat(df.Reference.astype(str), sep='_')
        t = df1.Region.str.cat(df1.Position.astype(str), sep='_').str.cat(df1.Reference.astype(str), sep='_')

        gain = 0
        loss = 0
        for element in list(s):
            if element in list(t):
                gain += 1
            else:
                loss += 1

        a = np.append(a, (i, gain, loss))
    res = pd.DataFrame(a.reshape(-1, 3), columns=['Dataset', 'Gain', 'Loss'])

    df = pd.read_csv('figures/2022_09_14/sites_HC_patients/'
                     'all_datasets/HealthySites.txt', sep='\t', header=0, low_memory=False)

    df1 = pd.read_csv('figures/2022_09_14/sites_HC_patients/'
                     'all_datasets/PatientSites.txt', sep='\t', header=0, low_memory=False)

    s = df.Region.str.cat(df.Position.astype(str), sep='_').str.cat(df.Reference.astype(str), sep='_')
    t = df1.Region.str.cat(df1.Position.astype(str), sep='_').str.cat(df1.Reference.astype(str), sep='_')

    gain = 0
    loss = 0
    for element in list(s):
        if element in list(t):
            gain += 1
        else:
            loss += 1