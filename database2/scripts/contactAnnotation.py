# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/10 16:24
# FileName: contactAnnotation
# Description:

import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database/results')


# def contactAnnotation():
#     lst = os.listdir('frequency/')
#
#     for i in lst:
#
#         df = pd.read_csv('%s/%s' % ('frequency', i), sep='\t', header=0)
#         anno = pd.read_csv('%s/%s.variant_function' % ('geneAnno/results/', i.split('.')[0]), sep='\t', header=0)
#
#         df = pd.concat([df.iloc[:, 0:6], anno, df.iloc[:, 6:]], axis=1).\
#             drop(columns=['X3','X4','X5','X6','X7'])


lst = os.listdir('frequency/')

for i in lst:
    df = pd.read_csv('%s/%s' % ('frequency', i), sep='\t', header=0)
    anno = pd.read_csv('%s/%s.variant_function' % ('geneAnno/results/', i.split('.')[0]), sep='\t', header=0)

    df = pd.concat([df.iloc[:, 0:6], anno, df.iloc[:, 6:]], axis=1).\
        drop(columns=['X3','X4','X5','X6','X7'])

    df = df.rename(columns={"X1": "region", "X2": 'annotation'})

    df.to_csv('%s/%s' % ('contactGeneFrequency', i), sep='\t', index=None)


lst = os.listdir('contactGeneFrequency/rename')
for i in lst:
    df = pd.read_csv('%s/%s' % ('contactGeneFrequency/rename', i), sep='\t', header=0)
    df['genes'] = df['genes'].str.split(',')
    df = df.explode('genes')
    df.to_csv('%s/%s' % ('contactGeneFrequency/explode', i), sep='\t', index=None)



lst = os.listdir('./desites')

for i in lst:
    df = pd.read_csv('%s/%s' % ('simplify_annotation', i), sep='\t', header=0)
    de = pd.read_csv('%s/%s' % ('desites', i), sep='\t', header=0)

    df1 = pd.merge(df.iloc[:, 0:7], de, on=['Region', 'Position', 'AllSubs'], how='left')
    df = pd.concat([df1, df.iloc[:, 7:]], axis=1).fillna('-')
    df.to_csv('%s/%s' % ('sitesAddDe', i), sep='\t', index=None)

