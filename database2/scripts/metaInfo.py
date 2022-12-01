# coding: utf-8
# Author: ryrl
# CreateTime: 2022/6/3 20:13
# FileName: metaInfo
# Description:

import os
import argparse
import pandas as pd


parser = argparse.ArgumentParser(description= 'scripts to process metaInfo')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar= 'directory', required= True,
                    help= 'The directory that contain metaInfo files')

parser.add_argument('--output', '-o',
                    dest= 'output', metavar= 'path',
                    required=True, help= 'where to save the final file')

args = parser.parse_args()
dire = args.directory
output = args.output

os.chdir('/public/workspace/ryrl/projects/upload/database/metaInfo')
dire = './'
lst = os.listdir(dire)

# cols = ['Run', 'disease', 'gender',
#         'A2GEditingIndex', 'ADAR', 'ADARB1',
#         'ADARB2', 'TNFa-nFkB', 'IL6-Jack-Stat3',
#         'INF-alpha','INF-gamma', 'Inflammatory', 'Complement', 'ISG']
df = pd.read_csv('%s/%s' % (dire, lst[1]), sep='\t', header=0)

for i in lst[1:]:
    df1 = pd.read_csv('%s/%s' % (dire, i), sep='\t', header=0)
    # if 'gender' not in df.columns:
    #     cols1 = cols.remove('gender')
    #     df1 = df1
    df = pd.concat([df, df1])
#
# lst1 = []
# for i in lst:
#     if i.startswith('ra'):
#         lst1.append(i)
#
# df = pd.read_csv('%s/%s' % (dire, lst1[0]), sep='\t', header=0)

# for i in lst:
#     df = pd.read_csv('%s/%s' % (dire, i), sep='\t', header=0)
#     if 'INF-alpha' not in df.columns:
#         print(i)

# df.columns = df.columns.str.replace('.', '-')
# df = df.rename(columns={'Alpha': 'INF-alpha', 'Gamma': 'INF-gamma'})
# df = df.rename(columns={'IFN-alpha': 'INF-alpha', 'IFN-gamma': 'INF-gamma'})
# df.to_csv('%s/%s' % (dire, lst[17]), sep='\t', index=None)

files = []
for i in lst:
    if i.startswith('ms'):
        files.append(i)

df = pd.read_csv('%s/%s' % (dire, files[0]), sep='\t', header=0)
df['dataset'] = files[0].split('_')[1]
df['number'] = '00'
count = 0
for i in files[1:]:
    count += 1
    number = str(count).rjust(2,'0')
    df1 = pd.read_csv('%s/%s' % (dire, i), sep='\t', header=0)
    df1['dataset'] = i.split('_')[1]
    df1['number'] = number
    df = pd.concat([df, df1])
    # if 'tissue' in df1.columns:
    #     print(i)

df = df.drop(columns=[
       'cell_surface_marker',
       'Collection', 'clinical_status', 'dmards_treatment', 'gsm', 'Condition',
       'ancestry', 'Instrument', 'tissue', 'anti-ro', 'cell_subtype',
       'sorting_markers', 'race', 'ancensty',
       'GEO sample ID', 'GEO descriptin for exp ID', 'flow_sort_selection',
       'id', 'Donor', 'treatment', 'Passage','Cell_type', 'sample',
       'AssemblyName', 'acpa_positivity'
]).fillna('-')

# df['test'] = df.index.astype(str)
# df['test'] = str(df['test']).rjust(2, '0')
df['test'] = ''
for i in range(0,977):
    df.iloc[i,21] = str(i).rjust(3,'0')

df['number1'] = df.number.str.cat(df.test, sep='-')



df['number2'] = df.index
for i in range(len(df.test)):
    df.iloc[i, len(df.columns) -1] = str(df.iloc[i, len(df.columns)-1]).rjust(3,'0')

df['number2'] = df.number.str.cat(df.number2, sep='-')
df = df.drop(columns=['test', 'ADARB2-AS1'])

df.to_csv('%s/%s' % ('./', 'metaInfo_all.txt'), sep='\t', index=None)
# df = pd.read_csv('%s/%s' % (dire, lst[0]), sep='\t', header=0)
# df1 = pd.read_csv('%s/%s' % (dire, lst[1]), sep='\t', header=0)
# df2 = pd.read_csv('%s/%s' % (dire, lst[2]), sep='\t', header=0)
# df3 = pd.read_csv('%s/%s' % (dire, lst[3]), sep='\t', header=0)
# df4 = pd.read_csv('%s/%s' % (dire, lst[4]), sep='\t', header=0)
# df5 = pd.read_csv('%s/%s' % (dire, lst[5]), sep='\t', header=0)
# df6 = pd.read_csv('%s/%s' % (dire, lst[6]), sep='\t', header=0)
# df7 = pd.read_csv('%s/%s' % (dire, lst[7]), sep='\t', header=0)
# df8 = pd.read_csv('%s/%s' % (dire, lst[8]), sep='\t', header=0)
# df9 = pd.read_csv('%s/%s' % (dire, lst[9]), sep='\t', header=0)
# df10 = pd.read_csv('%s/%s' % (dire, lst[10]), sep='\t', header=0)
# df11 = pd.read_csv('%s/%s' % (dire, lst[11]), sep='\t', header=0)
# df12 = pd.read_csv('%s/%s' % (dire, lst[12]), sep='\t', header=0)
# df13 = pd.read_csv('%s/%s' % (dire, lst[13]), sep='\t', header=0)
# df14 = pd.read_csv('%s/%s' % (dire, lst[14]), sep='\t', header=0)
# df15 = pd.read_csv('%s/%s' % (dire, lst[15]), sep='\t', header=0)
# df16 = pd.read_csv('%s/%s' % (dire, lst[16]), sep='\t', header=0)
# df17 = pd.read_csv('%s/%s' % (dire, lst[17]), sep='\t', header=0)
# df18 = pd.read_csv('%s/%s' % (dire, lst[18]), sep='\t', header=0)
# df19 = pd.read_csv('%s/%s' % (dire, lst[19]), sep='\t', header=0)
# df20 = pd.read_csv('%s/%s' % (dire, lst[20]), sep='\t', header=0)
# df21 = pd.read_csv('%s/%s' % (dire, lst[21]), sep='\t', header=0)



df = pd.read_csv('%s/%s' % ('./' , 'metaInfo_all.txt'),
                 sep='\t', header=0, low_memory=False)

for i in range(0,977):
    df['sample_id'][i] = str(i).rjust(2, '0')

df.to_csv('%s/%s' % ('./', 'metaInfo_all_test.txt'), sep='\t')