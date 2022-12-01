# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : coloclization_edQTLS.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/13 12:05
"""


import os
import pandas as pd

os.chdir('/public/workspace/ryrl/projects/upload/database3/data/snps')

edQTL = pd.read_csv('edQTL_GWAS_overlap_colocalizatic.txt', sep='\t', header=0, low_memory=False)

edQTL[['chr', 'start']] = edQTL.ref_SNP.str.split('_', expand=True)
edQTL = edQTL.sort_values(['chr', 'start'])
edQTL.chr = 'chr' + edQTL.chr


edQTL.to_csv('edQTL_GWAS_overlap_colocalizatic.txt', sep='\t', index=None)

annot = pd.read_csv('final.annot.txt', sep='\t', header=0, low_memory=False)
annot['#chr'] = 'chr' + annot['#chr']
annot['#chr'].value_counts()

mask = annot['#chr'] != 'chrX'
annot = annot[mask == True]
annot.to_csv('final.annot.txt', sep='\t', index=None)


res = pd.read_csv('../test1.tsv', sep='\t', header=None)
res.duplicated().value_counts()
res1 = res.drop_duplicates()
(res1[res1.columns[6]] < 100000).value_counts()