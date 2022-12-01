# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : mergeSitesWithSamplesNumber.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/24 08:19
"""


import os
import pandas as pd


if __name__ == '__main__':

    os.chdir('/public/workspace/ryrl/projects/upload/database3/data/Sites/Frequency/PA/addSupportSampleNumber')

    lst = os.listdir('./')

    df = pd.read_csv(lst[0], sep='\t', header=0, low_memory=False)
    mask = df.samplesSupport >= 20  # the number of patients to support the sites
    df = df[mask].drop(columns=['samplesSupport'])

    for i in lst[1:]:
        df1 = pd.read_csv(i, sep='\t', header=0, low_memory=False)
        mask = df1.samplesSupport >= 20
        df1 = df1[mask].drop(columns=['samplesSupport'])
        df = pd.merge(df, df1, on=['Region', 'Position', 'AllSubs'], how='outer')

    df.to_csv('/public/workspace/ryrl/projects/upload/database3/'
              'results/EditedGenes/mergeFrequencySample5/mergeFrequency.tsv', sep='\t', index=None)


    os.chdir('/public/workspace/ryrl/projects/upload/database3/results/EditedGenes')

    anno = pd.read_csv('%s/%s' % ('annotation/output', 'sites.hg38_multianno.txt'), sep='\t', header=0, low_memory=False)

    df = pd.concat([df.iloc[:, 0:3], anno.iloc[:, 5:8], df.iloc[:, 3:]], axis=1)
    df.to_csv('%s/%s' % ('final', 'edSites.tsv'), sep='\t', index=None)

    mask = df.Func_refGene == 'UTR3'
    df[mask].to_csv('final/UTR3.tsv', sep='\t', index=None)

    mask = df.Func_refGene == 'intronic'
    df[mask].to_csv('final/intronic.tsv', sep='\t', index=None)

    mask = df.Func_refGene == 'exonic'
    df[mask].to_csv('final/Exonic.tsv', sep='\t', index=None)