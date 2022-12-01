# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : cis_NATs.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/22 00:38
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/data/cis_NATs')

lst = os.listdir('./ori')

cis = pd.read_excel('%s/%s' % ('ori',lst[0]), skiprows=[0, 1, 2, 3])

for i in lst[1:]:
    df = pd.read_excel('%s/%s' % ('ori', i), skiprows=[0,1,2,3])
    cis = pd.concat([cis, df], axis=0)

mask = cis.cisNAT_ID.duplicated()
cis = cis[mask == False]

cis[['Ensemble1', 'Ensemble2']] = cis.cisNAT_ID.str.split('_', expand=True)[[0, 1]]
cis[['Symbol1', 'Symbol2']] = cis.Gene_Names.str.split('_', expand=True)[[0, 1]]
cis.columns
cis = cis.drop(columns=cis.columns[7:len(cis.columns)-5])
cis.to_csv('./concat/cis_NATs.tsv', sep='\t', index=None)



cis = pd.read_csv('./concat/cis_NATs.tsv', sep='\t', header=0)
cis.columns

cis2 = pd.read_excel('ori/cis-NATs.xlsx', comment='#')
cis2.columns
cis2['cis-NATs'].duplicated().value_counts()

cis[['Chr', 'Region']] = cis.Chr_Region.str.split(':', expand=True)
cis[['start', 'end']] = cis.Region.str.split('-', expand=True)
cis = cis.drop(columns=['Region'])
cis.to_csv('./concat/cis_NATs.tsv', sep='\t', index=None)

len(cis.columns)
cis = cis[cis.columns[11:14].append(cis.columns[0:10])]
cis = cis.iloc[:507, :]

mis = pd.read_excel('%s/%s' % ('ori', lst[5]), skiprows=[0,1,2,3])
mis = mis.rename(columns={mis.columns[1]: 'Chr',
                          mis.columns[2]: 'start',
                          mis.columns[3]: 'end'})
mis.Chr = 'chr' + mis.Chr.astype(str)
cis.columns
mis[['Ensemble1', 'Ensemble2']] = mis.cisNAT_ID.str.split('_', expand=True)[[0, 1]]

cis = pd.concat([cis, mis], axis=0).reset_index(drop=True)

cis[['Symbol1', 'Symbol2']] = cis.Gene_Names.str.split('_', expand=True)[[0, 1]]
cis = cis.drop(columns=['Symbol'])

cis = cis[cis.columns[0:13].append(cis.columns[[16]]).append(cis.columns[13:16])]

cis = cis.drop(columns=cis.columns[14:17])
cis = cis.sort_values(['Chr', 'start', 'end'])
cis.to_csv('./concat/cis_NATs.tsv', sep='\t', index=None)


cis = pd.read_csv('./concat/cis_NATs.tsv', sep='\t', header=0, low_memory=False)
mask = cis.Overlapping_Length >= 32
cis = cis[mask]
mask = cis.Overlapping_Length <= 1000
cis = cis[mask]

cis.to_csv('./concat/filter32_1000.tsv', sep='\t', index=None)

cis = pd.read_csv('./concat/filter32_1000.tsv', sep='\t', header=0, low_memory=False)
cis.start = cis.start.astype(int)
cis.end = cis.end.astype(int)

cis.to_csv('./concat/filter32_1000.tsv', sep='\t', index=None)



cis = pd.read_csv('./concat/filter32_1000.tsv', sep='\t', header=0, low_memory=False)
cis = cis.drop(columns=['Chr_Region'])
cis.to_csv('./concat/filter32_1000_drop.tsv', sep='\t', index=None, columns=None)

cis = pd.read_csv('./concat/filter32_1000.tsv', sep='\t', header=0)
liftover = pd.read_csv('./concat/cis_NATs_filtered32_1000_liftover.bed', sep='\t', header=None)

cis = pd.concat([liftover, cis.iloc[:, 5:]], axis=1)
cis.to_csv('./concat/cis_NATs_filtered32_1000_hg38.bed', sep='\t', index=None)