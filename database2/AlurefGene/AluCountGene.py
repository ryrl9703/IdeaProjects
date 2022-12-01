# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : AluCountGene.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/9/22 12:59
"""


import os
import argparse
import pandas as pd
import multiprocessing as mp

# gawk -F '\t' 'OFS="\t" {split($9,arr,";") split($18,b,";"); print $1,$2,$3,$4,$5,$6,$7,$8,arr[3],
# $10,$11,$12,$13,$14,$15,$16,$17,b[1],b[2]}' refGeneRmsk.txt > refGeneRmsk_split.txt
os.chdir('/public/workspace/ryrl/projects/upload/database2/AlurefGene')

df = pd.read_csv('./refGeneRmsk_split.txt', sep='\t', header=None)

df[df.columns[8]] = df[df.columns[8]].str.replace('gene_name ', '').str.replace('"', '')
df[df.columns[17]] = df[df.columns[17]].str.replace('gene_id ', '').str.replace('"', '')
df[df.columns[18]] = df[df.columns[18]].str.replace(' transcript_id ', '').str.replace('"', '')

df.to_csv('./refGeneRmsk_split_remove.txt', sep='\t', index=None, columns=None)


df = pd.read_csv('AluElement.txt', sep='\t', header=None)
test = df.iloc[:, [8, 18]].groupby(df.columns[8]).count()
test.head()

test.to_csv('./AluElementCount.txt', sep='\t')