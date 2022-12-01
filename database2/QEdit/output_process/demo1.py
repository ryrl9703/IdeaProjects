# coding: utf-8
# Author: ryrl
# CreateTime: 2022/3/3 19:34
# FileName: demo
# Description:


import os
import pandas as pd


os.chdir('/mnt/data/pcwang/RNA_edit/SLE/mouse/GSE146334/results/QEditing')

df = pd.read_csv('./OverallEditing.txt', sep=' ', header=0, skiprows=1)

df = df[df.index % 2 == 0]
df.TableName = df.TableName.str.split('/', expand=True)[1].str.split('.', expand=True)[0]
df = df.rename(columns={'TableName': 'Run'})


metaInfo = pd.read_csv('/mnt/data/pcwang/RNA_edit/SLE/mouse/GSE146334/info/metaInfo.tsv', sep='\t', header=0)

metaInfo = pd.merge(metaInfo, df, on=['Run'])

metaInfo.to_csv('./metaInfo.tsv', sep='\t', index=None)