# coding: utf-8
# Author: ryrl
# CreateTime: 2022/8/8 14:59
# FileName: qtl_GWAS
# Description:


import os
import pandas as pd


print('split files from ori Excel'.center(50, '='))
os.chdir('/public/workspace/ryrl/projects/upload/database2')

qtl = pd.read_excel(
    'qtl_gwas/ori/edQTL_GWAS_overlap_colocalizatic.xlsx', sheet_name=0, comment='#')

# qtl.columns
qtl[['Region', 'Position']] = qtl.EDITING_SITE.str.split('_', expand=True)
qtl.to_csv('./qtl_gwas/files/edQTL_gwas_overlap.tsv', sep='\t', index=None)


qtl = pd.read_excel(
    'qtl_gwas/ori/edQTL_GWAS_overlap_colocalizatic.xlsx', sheet_name=1, comment='#')

qtl[['snpRegion', 'snpPosition']] = qtl.ref_SNP.str.split('_', expand=True)
qtl.snpRegion = 'chr' + qtl.snpRegion
qtl.to_csv('./qtl_gwas/files/edQTL_gwas_coloc.tsv', sep='\t', index=None)



qtl = pd.read_excel(
    'qtl_gwas/ori/edQTL_GWAS_overlap_colocalizatic.xlsx', sheet_name=2, comment='#')

qtl[['snpRegion', 'snpPosition']] = qtl.ref_SNP.str.split('_', expand=True)
qtl.snpRegion = 'chr' + qtl.snpRegion
qtl.to_csv('./qtl_gwas/files/eQTL_gwas_coloc.tsv', sep='\t', index=None)


qtl = pd.read_excel(
    'qtl_gwas/ori/edQTL_GWAS_overlap_colocalizatic.xlsx', sheet_name=3, comment='#')

qtl[['snpRegion', 'snpPosition']] = qtl.ref_SNP.str.split('_', expand=True)
qtl.snpRegion = 'chr' + qtl.snpRegion

qtl[['qtlRegion', 'qtlStart', 'qtlEnd', 'clu']] = qtl.QTL_feature.str.split(':', expand=True)
qtl.qtlRegion = 'chr' + qtl.qtlRegion

qtl.to_csv('./qtl_gwas/files/sQTL_gwas_coloc.tsv', sep='\t', index=None)



cis = pd.read_excel('qtl_gwas/ori/cis-NATs.xlsx', comment='#')

cis[['snpRegion', 'snpPosition']] = cis.ref_SNP.str.split('_', expand=True)
cis.snpRegion = 'chr' + cis.snpRegion

# qtl[['qtlRegion', 'qtlStart', 'qtlEnd', 'clu']] = qtl.QTL_feature.str.split(':', expand=True)
# qtl.qtlRegion = 'chr' + qtl.qtlRegion

qtl.to_csv('./qtl_gwas/files/cis-NAT.tsv', sep='\t', index=None)


print('EditingSites match QTL and GWAS'.center(50, '='))

os.chdir('/public/workspace/ryrl/projects/upload/database2')
dirs = os.listdir()
os.listdir('%s/%s' % (dirs[2], 'files'))

qtl = pd.read_csv('%s/%s/%s' % (dirs[2], 'files', 'edQTL_gwas_overlap.tsv'), sep='\t', header=0, low_memory=False)
edSites = pd.read_csv('finalResults/editingSites/RheumatoidArthritis.txt', sep='\t', header=0, low_memory=False)

# qtl.columns
# edSites.columns

# ra = qtl.loc[(qtl['DISEASE/TRAIT'] == 'Rheumatoid arthritis') == True, :]
#
# df = pd.merge(edSites, ra, how='left', on=['Region', 'Position'])
#
# df.Reference.fillna('-').value_counts()

edSites.columns
edSites.iloc[:, [0,1,1,3]]
df = edSites.iloc[:, [0,1,1,3]]  #.to_csv('./tmp/edSites.txt', sep='\t', index=None)
df.iloc[:, 2] = df.iloc[:, 2] + 1
df.to_csv('./tmp/edSites.txt', sep='\t', index=None)

df1 = qtl.loc[:, ['CHR_ID', 'CHR_POS', 'CHR_POS', 'SNPS']]
df1.CHR_ID.notna().value_counts()

df1 = df1.loc[df1.CHR_ID.notna() == True, :]

df1.CHR_ID = 'chr' + df1.CHR_ID.astype(int).astype(str)
df1.CHR_POS = df1.CHR_POS.astype(int)
df1.iloc[:, 2] = df1.iloc[:, 2] + 1
# df.sort_values(by )
df1.columns
df1 = df1.drop_duplicates(subset = ['SNPS'], keep='first', ignore_index=True)

df1.to_csv('./tmp/qtl.txt', sep='\t', index=None)


print(''.center(100, '='))
# qtl = pd.read_csv('%s/%s/%s' % ('qtl_gwas', 'files', 'edQTL_gwas_overlap.tsv'), sep='\t', header=0, low_memory=False)
os.chdir('/public/workspace/ryrl/projects/upload/database2')
dirs = os.listdir('diseases_natural')

for i in dirs:
    if os.path.exists('%s/%s/%s.txt' % ('finalResults', 'editingSites', i)):
        qtl = pd.read_csv('%s/%s/%s' % ('diseases_natural', i, 'edQTL_gwas_overlap.tsv'),
                          sep='\t', header=0, low_memory=False)
        edSites = pd.read_csv('%s/%s/%s.txt' % ('finalResults', 'editingSites', i),
                              sep='\t', header=0, low_memory=False)

        edSites = edSites.iloc[:, [0,1,1,3]]
        edSites.iloc[:, 2] = edSites.iloc[:, 2] + 1
        edSites.to_csv('%s/%s/edSites.txt' % ('diseases_natural', i), sep='\t', index=None)


        qtl = qtl.loc[:, ['CHR_ID', 'CHR_POS', 'CHR_POS', 'SNPS']]
        # df1.CHR_ID.notna().value_counts()

        qtl = qtl.loc[qtl.CHR_ID.notna() == True, :]

        qtl.CHR_ID = 'chr' + qtl.CHR_ID.astype(int).astype(str)
        qtl.CHR_POS = qtl.CHR_POS.astype(int)
        qtl.iloc[:, 2] = qtl.iloc[:, 2] + 1

        qtl = qtl.drop_duplicates(subset = ['SNPS'], keep='first', ignore_index=True)

        qtl.to_csv('%s/%s/SNPs.txt' % ('diseases_natural', i), sep='\t', index=None)
    else:
        print('%s/%s/%s is not exit' % ('finalResults', 'editingSites', i))



df = pd.read_csv('qtl_gwas/files/cis-NAT.tsv', sep='\t', header=0, low_memory=False)
df.columns
len(df.gene_name.drop_duplicates())
df.GWAS_trait.value_counts()


print('edSites coloc'.center(50, '='))

dirs = os.listdir('diseases_natural')


# qtl = pd.read_csv('%s/%s/%s' % ('diseases_natural', i, 'edSites_coloc.txt'),
#                   sep='\t', header=0, low_memory=False)
# qtl.columns
# qtl = qtl.loc[:, ['gene_name', 'snpRegion', 'snpPosition', 'snpPosition']]
# qtl.iloc[:, 3] = qtl.iloc[:, 3] + 1
for i in dirs:
    if os.path.exists('%s/%s/%s.txt' % ('finalResults', 'editingSites', i)):
        edSites = pd.read_csv('%s/%s/%s.txt' % ('finalResults', 'editingSites', i),
                              sep='\t', header=0, low_memory=False)
        qtl = pd.read_csv('%s/%s/%s' % ('diseases_natural', i, 'edSites_coloc.txt'),
                          sep='\t', header=0, low_memory=False)

        qtl = qtl.loc[:, ['snpRegion', 'snpPosition', 'snpPosition', 'gene_name']]
        qtl.iloc[:, 2] = qtl.iloc[:, 2] + 1

        qtl.to_csv('%s/%s/edSites_coloc_snp.txt' % ('diseases_natural', i), sep='\t', index=None)
    else:
        print('%s/%s/%s is not exit' % ('finalResults', 'editingSites', i))