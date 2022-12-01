# coding: utf-8
# Author: ryrl
# CreateTime: 2022/5/30 16:12
# FileName: sites_merge_disease
# Description:


# TODO code redundancy
import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description= 'scripts to merge sites by datasets')

parser.add_argument('--disease', '-d', dest='disease',
                    metavar= 'disease', required= True,
                    help= 'The disease that the script to process, a directory')

parser.add_argument('--site', '-s',
                    dest='site', metavar='type',
                    required= True, choices= ['redi', 'recoding'],
                    help= 'The site type you want to process, choose from redi and recoding')

# parser.add_argument('--metaInfo', '-m',dest='metaInfo',
#                     metavar='sample information',required= True,
#                     choices= ['metaInfo', 'sample_status'],
#                     help= 'The file that contain sample information, choose from metaInfo and sample_status')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, default= '~/projects/upload/database/sites',
                    help= 'where to save the final file')
args = parser.parse_args()
disease = args.disease
siteType = args.site
# metaInfo = args.metaInfo
output = args.output



lst = []
for i in os.listdir(disease):
    if i.__contains__(siteType):
        lst.append(i)
if siteType == 'redi':
    site = pd.read_csv('%s/%s' % (disease, lst[0]), sep='\t', header=0)
elif siteType == 'recoding':
    site = pd.read_csv('%s/%s' % (disease, lst[0]), sep='\t', header=0).drop(columns=['MeanFrequency', 'Frequency_all'])

for j in lst[1:]:
    if siteType == 'redi':
        df = pd.read_csv('%s/%s' % (disease, j), sep='\t', header=0)
        site = pd.merge(site, df, how='outer', on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs'],
                        suffixes=('', j.split('_')[0]))

        site = site.fillna(0)
        lst = []
        for i in site.columns:
            if i.startswith('MeanFrequency'):
                lst.append(i)

        site['MeanFrequency'] = site[lst].mean(axis=1)
        site = site.drop(columns=lst[1:])

        lst = []
        for i in site.columns:
            if i.startswith('Frequency'):
                lst.append(i)

        for i in lst[1:]:
            site['Frequency_all'] = site['Frequency_all'].astype(str).str.cat(site.loc[:, i].astype(str), sep=';')
        site = site.drop(columns=lst[1:])

    elif siteType == 'recoding':
        df = pd.read_csv('%s/%s' % (disease, i), sep='\t', header=0).drop(columns=['MeanFrequency', 'Frequency_all'])
        site = pd.merge(site, df, how='outer', on=['Region', 'Position', 'Reference', 'Strand', 'AllSubs', 'siteType'],
                        suffixes=('', i.split('_')[0]))

if disease.split('/')[-1] == '':
    name = disease.split('/')[-2]
else:
    name = os.path.basename(disease)

site.to_csv('%s/%s_%s.txt' % (output, name, siteType), sep='\t', index=None)