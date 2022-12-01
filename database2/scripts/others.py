# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/15 9:09
# FileName: others
# Description:

import os
import pandas as pd


os.chdir('/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset/InflammatoryBowelDisease')

df1 = pd.read_csv('./GSE158952.txt', sep='\t', header=0, low_memory=False)
df2 = pd.read_csv('./GSE171770.txt', sep='\t', header=0, low_memory=False)

df = pd.merge(df1, df2,
              on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'type'], how='outer')

# df.to_csv('../../merge_each_disease/InflammatoryBowelDisease.txt', sep='\t', index=None)


anno1 = pd.read_csv('./GSE158952_toAnno.txt.variant_function', sep='\t', header=None, low_memory=False)
anno1['genes'] = anno1.iloc[:,1].str.split('(', expand=True)[0]
df1 = pd.concat([df1.iloc[:, 0:6], anno1.iloc[:, [0, 1, 7]], df1.iloc[:, 6:]], axis=1)
# df1.to_csv('./GSE158952.contact.txt', sep='\t', index=None)


anno2 = pd.read_csv('./GSE171770_toAnno.txt.variant_function', sep='\t', header=None, low_memory=False)
anno2['genes'] = anno2.iloc[:, 1].str.split('(', expand=True)[0]
df2 = pd.concat([df2.iloc[:, 0:6], anno2.iloc[:, [0, 1, 7]], df2.iloc[:, 6:]], axis=1)
# df2.to_csv('./GSE171770.contact.txt', sep='\t', index=None)


tpm1 = pd.read_csv('/public/workspace/ryrl/projects/rnaedit_autoimmune/data/inflammatory_bowel_disease/GSE158952/matrix/tpm.txt', sep='\t', header=0, low_memory=False)
genes = df1['genes'].str.split(',').explode().drop_duplicates()
index = tpm1.index.isin(genes)
geneEditedTpm = tpm1[index]
df1['genes'] = df1['genes'].str.split(',')
df1 = df1.explode('genes')
editedSitesMergeTpm = pd.merge(df1.iloc[:, 0:9], geneEditedTpm,
                               left_on=['genes'], right_index=True, how='left')
# editedSitesMergeTpm.to_csv(
#     '../../../results/genesEditedTpmByDataSet/ori/inflammatory_bowel_disease_GSE158952_geneEditedTpm.txt', sep='\t', index=None
# )
# geneEditedTpm.to_csv(
#     '../../../results/genesEditedTpmByDataSet/ori/InflammatoryBowelDisease_GSE158952_geneEditedTpm.txt', sep='\t', index=True)


tpm2 = pd.read_csv('/public/workspace/ryrl/projects/rnaedit_autoimmune/data/inflammatory_bowel_disease/GSE171770/matrix/tpm.txt', sep='\t', header=0, low_memory=False)
genes = df1['genes'].str.split(',').explode().drop_duplicates()
index = tpm2.index.isin(genes)
geneEditedTpm = tpm2[index]
df2['genes'] = df2['genes'].str.split(',')
df2 = df2.explode('genes')
editedSitesMergeTpm = pd.merge(df2.iloc[:, 0:9], geneEditedTpm,
                               left_on=['genes'], right_index=True, how='left')
editedSitesMergeTpm.to_csv(
    '../../../results/genesEditedTpmByDataSet/ori/inflammatory_bowel_disease_GSE171770_geneEditedTpm.txt', sep='\t', index=None
)
# geneEditedTpm.to_csv(
#     '../../../results/genesEditedTpmByDataSet/ori/InflammatoryBowelDisease_GSE171770_geneEditedTpm.txt', sep='\t', index=True)


os.chdir('/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset/MultipleSclerosis')

df1 = pd.read_csv('./GSE172009.txt', sep='\t', header=0, low_memory=False)
anno1 = pd.read_csv('./GSE172009_toAnno.txt.variant_function', sep='\t', header=None, low_memory=False)
anno1['genes'] = anno1.iloc[:,1].str.split('(', expand=True)[0]
df1 = pd.concat([df1.iloc[:, 0:6], anno1.iloc[:, [0, 1, 7]], df1.iloc[:, 6:]], axis=1)


os.chdir('/public/workspace/ryrl/projects/upload/database/finalResults')

df = pd.read_csv('/public/workspace/ryrl/projects/upload/database/sites/split/InflammatoryBowelDisease_frequency.txt', sep='\t', header=0)

df1 = df.iloc[:, 6:]

for i in df1.columns:
    mask = df1[i].isna()
    df1[i][mask == False] = i

df1 = df1.fillna('-')


for i in df1.columns[1:]:
    df1['ibd-026-1372-ibd'] = df1['ibd-026-1372-ibd'].str.cat(df1[i], sep=';')

df2 = pd.concat([df.iloc[:, 0:6], df1.iloc[:, 0]], axis=1)
df2 = df2.rename(columns={'ibd-026-1372-ibd': 'samples'})

de = pd.read_csv('/public/workspace/ryrl/projects/upload/database/finalResults/sitesAddDe/InflammatoryBowelDisease.txt', sep='\t', header=0)


de = pd.concat([de.iloc[:, 0:6], df2.iloc[:, 6], de.iloc[:, 6:]], axis=1)
de['samples'] = de['samples'].str.replace('-;', '')
de['samples'] = de['samples'].str.replace(';-', '')
de.to_csv('./InflammatoryBowelDisease.txt', sep='\t', index=None)



os.chdir('/public/workspace/ryrl/projects/upload/database/finalResults/sitesAddDe')
cols = ['regsnp_splicing_site', 'regsnp_fpr', 'regsnp_disease', 'snp151_tid']
lst = os.listdir('./')

for i in lst:
    df = pd.read_csv(i, sep='\t', header=0, low_memory=False)
    df = df.drop(columns=cols)
    df.to_csv(i, sep='\t', index=None)

df = pd.read_csv(lst[5], sep='\t', header=0, low_memory=False)
df = df.drop(columns=['refGene_feat', 'refGene_gid', 'refGene_tid'])
df.to_csv(lst[5], sep='\t', index=None)


de = pd.read_csv('../tmp/InflammatoryBowelDisease.txt.hg38_multianno.txt', sep='\t', header=0)
df = pd.concat([df.iloc[:, 0:14], de.iloc[:, 5:], df.iloc[:, 14:]], axis=1)
df = df.drop(columns=df.columns[19:])
df.to_csv(lst[5], sep='\t', index=None)


os.chdir('/public/workspace/ryrl/projects/upload/database/finalResults/frequency')

df = pd.read_csv('Psoriasis.txt', sep='\t', header=0, low_memory=False)
df1 = df.iloc[:, 6:]
for i in df1.columns:
    mask = df1[i].isna()
    df1[i][mask == False] = i

df1 = df1.fillna('-')


for i in df1.columns[1:]:
    df1.iloc[:, 0] = df1.iloc[:, 0].str.cat(df1[i], sep=';')

df2 = pd.concat([df.iloc[:, 0:6], df1.iloc[:, 0]], axis=1)
df2 = df2.rename(columns={'pso-016-0829-pso': 'samples'})

de = pd.read_csv('../../results/desites/Psoriasis.txt', sep='\t', header=0)

df2 = pd.merge(df2, de, on=['Region', 'Position', 'AllSubs'], how='left')
df2 = df2.fillna('-')

df2.samples = df2.samples.str.replace('-;','')
df2.samples = df2.samples.str.replace(';-', '')

# anno1 = pd.read_csv('../editingSites/Psoriasis.txt', sep='\t', header=0, low_memory=False)


df2.to_csv('../editingSites/Psoriasis.txt', sep='\t', index=None)


df = pd.read_csv('../Psoriasis.refGene.rmsk.snp151.txt', sep='\t', header=0)
de = pd.read_csv('../tmp/Psoriasis.hg38_multianno.txt', sep='\t', header=0)

df = pd.concat([df, de.iloc[:, 5:]], axis=1)
df = df.drop(columns=['refGene_feat', 'refGene_gid', 'refGene_tid','regsnp_fpr','regsnp_disease', 'regsnp_splicing_site'])
df.to_csv('../editingSites/Psoriasis.txt', sep='\t', index=None)


df = pd.read_csv(lst[0], sep=' ', header=None)

for i in lst[1:]:
    de = pd.read_csv(i, sep=' ', header=None)
    df = pd.concat([df, de], axis=0)
df.iloc[:, 1] = df.iloc[:, 1].str.split('/', expand=True)[3]
df.iloc[:,1] = df.iloc[:, 1].str.replace('.tsv', '')
df = df.rename(columns={df.columns[0]: 'sitesCount', df.columns[1]: 'Run'})
df.to_csv('/public/workspace/ryrl/projects/upload/database/results/metaInfo/sitesCount.txt', sep='\t', index=None)

df = pd.read_csv('/public/workspace/ryrl/projects/upload/database/results/metaInfo/sitesCount.txt', sep='\t', header=0)
df['sitesCount'] = df['sitesCount'] - 1

metaInfo = pd.read_csv('/public/workspace/ryrl/projects/upload/database/results/metaInfo/metaInfo_all.txt', sep='\t', header=0)
metaInfo = metaInfo.drop(columns=['sitesCount'])


metaInfo = pd.merge(metaInfo, df, on=['Run'], how='left')
metaInfo.to_csv('/public/workspace/ryrl/projects/upload/database/results/metaInfo/metaInfo_all.txt', sep='\t', index=None)


os.chdir('/public/workspace/ryrl/liftOver/hg19Tohg38/TranscriptionFactorBindingSite')
ori = pd.read_csv('./hg19_tfbsConsSites.txt', sep='\t', header=None)
ori = ori.iloc[:, [0,1,4,5,6,7]]
ori = ori.rename(columns={ori.columns[0]: 'A',
                          ori.columns[1]: 'B',
                          ori.columns[2]: 'C',
                          ori.columns[3]: 'D',
                          ori.columns[4]: 'E',
                          ori.columns[5]: 'F'})
df = pd.read_csv('./hg38_tfbsConsSites.txt', sep='\t', header=None)
df = df.rename(columns={df.columns[0]: 'B',
                        df.columns[3]: 'C',
                        df.columns[4]: 'D',
                        df.columns[5]: 'E',
                        df.columns[6]: 'F'})


df1 = pd.merge(ori,df, on=['C', 'D', 'E', 'F'], how='right')
