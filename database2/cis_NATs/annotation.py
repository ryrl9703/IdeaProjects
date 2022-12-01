# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : annotation.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/1 08:27
"""


import os
import pandas as pd


if __name__ == '__main__':

    os.chdir('/public/workspace/ryrl/projects/upload/database3/results/Sites/Diseases/HC/annotation')

    lst = os.listdir('annovar/out')

    for i in lst:

        annovar = pd.read_csv('%s/%s' % ('annovar/out', i), sep='\t', header=0, low_memory=False)
        redi = pd.read_csv('%s/%s.refGene.rmsk.snp151.txt' % ('snp151', i.split('.')[0]), sep='\t', header=0, low_memory=False)

        df = pd.concat([redi.iloc[:, :3], annovar.iloc[:, 5:8], redi.iloc[:, 3:]], axis=1)

        df.to_csv('concat/%s.tsv' % i.split('.')[0], sep='\t', index=None)


    print('Annotation sites in cis-NATs genes'.center(100, '='))

    cis = pd.read_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database3/'
                                 'results/cis_NATs_related/sitesIncis_NATs/PA', 'Coeliac.tsv'), sep='\t', header=None, low_memory=False)

    cis.duplicated(cis.columns[13:16]).value_counts()


    df = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/results/cis_NATs_related/SitesByDisease/HC/sites/Coeliac.tsv', sep='\t', header=None)