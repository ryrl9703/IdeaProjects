# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : eiditngSitesNumber.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/11/25 10:04
"""

import os
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def unpivot(frame, col1:str, col2:str, col3:str):
    N, K = frame.shape
    data = {
        col3: frame.to_numpy().ravel("F"),
        col2: np.asarray(frame.columns).repeat(N),
        col1: np.tile(np.asarray(frame.index), K),
    }
    return pd.DataFrame(data, columns=[col1, col2, col3])


def merge_sites_by_status(dirs:str) -> pd.DataFrame:
    """

    :param dirs:
    :return:
    """

    lst = os.listdir(dirs)
    df = pd.read_csv('%s/%s' % (dirs, lst[0]), sep='\t', header=0, low_memory=False).iloc[:, 0:4]

    for i in lst[1:]:

        s = pd.read_csv('%s/%s' % (dirs, i), sep='\t', header=0, low_memory=False).iloc[:, 0:4]

        df = pd.merge(df, s, on=['Region', 'Position', 'AllSubs', 'Func_refGene'], how='outer')

    return df


def count_Sites(dir1:str, dir2:str) -> pd.DataFrame:
    """

    :param dir1: Healthy
    :param dir2: Patient
    :return:
    """

    global h
    lst = os.listdir(dir2)

    s = pd.DataFrame()
    for i in lst:

        if os.path.exists('%s/%s' % (dir1, i)):

            h = pd.read_csv('%s/%s' % (dir1, i), sep='\t', header=0, low_memory=False)
            h.AllSubs = h.AllSubs.str.split(' ', expand=True)[0]
            h = pd.DataFrame(h.AllSubs.value_counts())
            h = h.rename(columns={'AllSubs': '%s_Healthy' % i.split('.')[0]})
        else:
            print('%s has no healthy sample' % i.split('.')[0])

        p = pd.read_csv('%s/%s' % (dir2, i), sep='\t', header=0, low_memory=False)
        p.AllSubs = p.AllSubs.str.split(' ', expand=True)[0]
        p = pd.DataFrame(p.AllSubs.value_counts())
        p = p.rename(columns={'AllSubs': '%s_Patient' % i.split('.')[0]})

        s = pd.concat([s, h, p], axis=1)

    return s

def count_region_by_disease(dirs:str, col:str) -> pd.DataFrame:
    """

    :param col:
    :param dirs:
    :return:
    """

    lst = os.listdir(dirs)

    df = pd.DataFrame()
    for i in lst:
        s = pd.read_csv('%s/%s' % (dir1, i), sep='\t', header=0, low_memory=False)

        if col == 'rmsk_tid':
            s[col] = s[col].apply(lambda x: x if x == '-' else x.split('-')[0])
            s[col] = s[col].apply(lambda x: x if x == 'Alu' or x == 'L1' else 'Other')
        elif col == 'Func_refGene':
            s[col] = s[col].str.split(';', expand=True)[0]

        s = pd.DataFrame(s[col].value_counts())
        s = s.rename(columns={col: i.split('.')[0]})

        df = pd.concat([df, s], axis=1)
    return df



if __name__ == '__main__':

    print('#edSitings'.center(100, '='))
    dir1 = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Diseases/HC/remove_chrXYM'
    dir2 = '/public/workspace/ryrl/projects/upload/database3/results/Sites/Diseases/PA/remove_chrXYM'
    # i = lst[0]
    # col = 'rmsk_tid'
    # col = 'Func_refGene'

    # df = merge_sites_by_status('/public/workspace/ryrl/projects/upload/database3/results/Sites/DataSet/PA/remove_chrXYM')
    # df_HC = merge_sites_by_status('/public/workspace/ryrl/projects/upload/database3/results/Sites/DataSet/HC/remove_chrXYM')
    #
    # # penguins = sns.load_dataset('penguins')
    #
    # df.AllSubs = df.AllSubs.str.split(' ', expand=True)[0]
    # df_HC.AllSubs = df.AllSubs.str.split(' ', expand=True)[0]
    #
    # p = pd.DataFrame(df.AllSubs.value_counts())
    # p = p.rename(columns = {'AllSubs': 'Patient'})
    #
    # h = pd.DataFrame(df_HC.AllSubs.value_counts())
    # h = h.rename(columns={'AllSubs': 'Healthy'})
    #
    # s = pd.concat([p, h], axis=1)
    # s = unpivot(s)


    s = count_Sites(dir1, dir2)
    t = unpivot(s).dropna()

    t[['Disease', 'Status1']] = t.Status.str.split('_', expand=True)

    t.to_csv('%s/%s' % ('/public/workspace/ryrl/projects/upload/database3/figures/2022_11_25/data', 'sitesNumber.tsv'), sep='\t', index=True)

    # mask = t.Disease == 'MS'
    tips = sns.load_dataset('tips')

    # g = sns.FacetGrid(t, col= 'Disease')
    # g.map(sns.catplot, 'bar','AllSubs', 'Value', 'Status1')
    # plt.show()

    # g = sns.FacetGrid(t, hue='Status1', col='Disease')
    # g.map(sns.barplot, 'AllSubs', 'Value')
    # plt.show()


    fig = sns.catplot(data=t, kind='bar',
                      x='AllSubs', y='Value',
                      col='Disease',hue='Status1',
                      errorbar='sd', palette='dark', alpha=.6, height=6)
    fig.set_titles(fontsize=14)
    plt.show()

    fig.savefig('/public/workspace/ryrl/projects/upload/database3/figures/2022_11_25/data/test.pdf', dpi=300)

    print('AluElements percentage'.center(100, '='))

    df = count_region_by_disease(dir1, 'rmsk_tid')
    df.index = df.index + '_Healthy'

    df1 = count_region_by_disease(dir2, 'rmsk_tid')
    df1.index = df1.index + '_Patient'

    df = pd.concat([df.T, df1.T], axis=1)

    df = unpivot(df, 'Disease', 'Status', 'Value').dropna()

    df[['RepeatElement', 'Status1']] = df.Status.str.split('_', expand=True)


    de = df.set_index(['Status1', 'Disease', 'RepeatElement']).iloc[:, 1].unstack()

    # fig, ax = plt.subplots(4, 2)
    #
    #
    # for i in range(2):
    #     for j in range(2):
    #         ax[i, j] =

    labels = 'Alu', 'L1', 'Other'
    for i in range(de.shape[0]):

        fracs = de.iloc[i, :].to_list()
        fig, ax = plt.subplots()
        explode = (0.1, 0, 0)
        ax.pie(fracs, labels=labels, autopct='%1.1f%%', explode=explode, shadow=True)
        ax.axis('equal')
        ax.set_title(de.iloc[i, :].name[1], fontsize=20)
        fig.savefig('/public/workspace/ryrl/projects/upload/database3/'
                    'figures/2022_11_25/plots/%s_%s.pdf' % (de.iloc[i, :].name[1], de.iloc[i, :].name[0]), dpi=300)


    print('UTR3'.center(100, '='))

    df = count_region_by_disease(dir1, 'Func_refGene')
    df.columns = df.columns + '-Healthy'

    df1 = count_region_by_disease(dir2, 'Func_refGene')
    df1.columns = df1.columns + '-Patient'

    df = pd.concat([df, df1], axis=1)
    de = unpivot(df, 'Region', 'Disease', 'Value').dropna()

    de[['Disease1', 'Status']] = de.Disease.str.split('-', expand=True)

    # de = df.set_index(['Status', 'Disease', 'Region1']).iloc[:, 1].unstack()

    fig = sns.catplot(data=de, kind='bar',
                      x='Region', y='Value',
                      col='Disease1', hue='Status',
                      errorbar='sd', palette='dark', alpha=.6, height=6)
    # fig.set_titles(fontsize=14)
    # fig.xticks(rotation=90)
    # plt.show()

    fig.savefig('/public/workspace/ryrl/projects/upload/database3/figures/2022_11_25/data/UTR3.pdf', dpi=300)


    mask = de.Disease1 == 'MS'
    s = de[mask]

    s.refGene_feat.value_counts()

    sns.catplot(data=s, kind='bar',
                x='Region', y='Value',
                col='Disease1', hue='Status',
                errorbar='sd', palette='dark', alpha=.6, height=6, roatation=90)
    plt.show()


    mask = s.refGene_feat.str.contains('3UTR')
    # s.refGene_feat.apply(lambda x: 'UTR3' if x.contians('3UTR') else x, axis=0)

    # s['refGene_feat'].apply(lambda x: 'UTR3' if x.contain('3UTR') else x)
    # s.refGene_feat.str.split(',', expand=True)[0].value_counts()
    s.iloc[s[mask].refGene_feat.index, 6] = 'UTR3'

    s.refGene_feat.str.split(',', expand=True)[0].str.split('$', expand=True)[0].str.split('&', expand=True)[0].value_counts()
