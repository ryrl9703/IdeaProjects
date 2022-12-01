# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : Oncoprint.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/3 08:05
"""

import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/'
          'results/cis_NATs_related/cis_NATs_intersect_edSites/ByDisease/PA')


lst = os.listdir('./')

df = pd.read_csv(lst[0], sep='\t', header=None, low_memory=False)
df = df.rename(columns={df.columns[25]: lst[0].split('.')[0]})
df.iloc[:, 25] = df.iloc[:, 25].str.split('-', expand=True)[0]

mask = df.iloc[:, 25] != 'Alu'
df.iloc[:, 25][mask] = 'Others'
# df.iloc[:, [25][mask == False] = 1
df = df.iloc[:, []]
df.iloc[:, 5].drop_duplicates().value_counts()


for i in lst[1:]:
    df1 = pd.read_csv(i, sep='\t', header=None, low_memory=False)
    df1 = df1.rename(columns={df1.columns[25]: i.split('.')[0]})
    df1.iloc[:, 25] = df1.iloc[:, 25].str.split('-', expand=True)[0]

    mask = df1.iloc[:, 25] != 'Alu'
    df1.iloc[:, 25][mask] = 'Others'
    # df1.iloc[:, 25][mask == False] = 1
    df1 = pd.DataFrame(df1[i.split('.')[0]])


    # df = pd.merge(df, df1, left_index=True, right_index=True, how='outer')
    df = pd.concat([df, df1], axis=1)

df.to_csv('../density.tsv', sep='\t', index=None)


os.chdir('/public/workspace/ryrl/projects/upload/database2/rediTable/filtered/filter_5_1/ori')

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database3/'
                       'data/metaInfo/metaInfo_IFNscore_HallMarkscores_1023.txt', sep='\t', header=0, low_memory=False)


lst = list(set(metaInfo.Disease_id))

# lst = os.listdir('./')
# for i in lst[:]:
#     if i not in list(metaInfo.Run):
#         lst.remove(i)

# df = pd.read_csv('%s/%s.tsv' % (lst[0], lst[0]), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,4]]
# df.rename(columns={'Coverage-q30': lst[0]})

for i in lst:
    srr = metaInfo[metaInfo.Disease_id == i].Run.to_list()

    df = pd.read_csv('%s/%s.tsv' % (srr[0], srr[0]), sep='\t', header=0, low_memory=False).iloc[:, [0, 1, 7, 4]]
    df.rename(columns={'Coverage-q30': srr[0]})

    for j in srr[1:]:
        if os.path.exists('%s/%s' % (j, j)):

            de = pd.read_csv('%s/%s.tsv' % (j, j), sep='\t', header=0, low_memory=False).iloc[:, [0,1,7,4]]
            de = de.rename(columns={'Coverage-q30': j})

            df = pd.merge(df, de, on=['Region', 'Position', 'AllSubs'], how='outer')
        else:
            continue

    df.to_csv('%s/%s.tsv' % ('/public/workspace/ryrl/projects/upload/database3/results/Sites/Coverage/ByDataset', i), sep='\t', index=None)
