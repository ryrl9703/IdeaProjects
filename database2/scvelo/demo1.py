# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : demo.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/10/25 21:58
"""


import anndata
import scvelo as scv
import pandas as pd
import numpy as np
import velocyto as vly
import matplotlib as plt


if __name__ == '__main__':

    sample_one = anndata.read_loom("/public/workspace/danhuasu127/project/"
                                   "sigcell/7_dsDNA/01_data/F_velocyto_loom/conCD4_out.loom")

    sample_one.var_names_make_unique()

    sample_two = anndata.read_loom("/public/workspace/danhuasu127/project/"
                                   "sigcell/7_dsDNA/01_data/F_velocyto_loom/trialCD4_2w_out.loom")
    sample_two.var_names_make_unique()
    sample_three = anndata.read_loom("/public/workspace/danhuasu127/project/"
                                     "sigcell/7_dsDNA/01_data/F_velocyto_loom/trialCD4_6w_out.loom")
    sample_three.var_names_make_unique()

    sample_obs = pd.read_csv("/public/workspace/danhuasu127/project/"
                             "sigcell/7_dsDNA/01_data/G_ananlysis_data/02_analysis2_data/05_RNA_velocity/cellID_obs.csv")
    umap = pd.read_csv("/public/workspace/danhuasu127/project/"
                       "sigcell/7_dsDNA/01_data/G_ananlysis_data/02_analysis2_data/05_RNA_velocity/cell_embeddings.csv")
    cell_clusters = pd.read_csv("/public/workspace/danhuasu127/project/"
                                "sigcell/7_dsDNA/01_data/G_ananlysis_data/02_analysis2_data/05_RNA_velocity/clusters_obs.csv")

    sample_one = sample_one[np.isin(sample_one.obs.index, sample_obs["x"])]
    sample_two = sample_two[np.isin(sample_two.obs.index, sample_obs["x"])]

    adata = sample_one.concatenate(sample_two, sample_three)

    adata_index = pd.DataFrame(adata.obs.index)

    adata_index = adata_index.rename(columns={0: 'Cell ID'})
    adata_index = adata_index.rename(columns={"CellID": 'Cell ID'})
    adata_index = adata_index.rename(columns={adata_index.columns[0]: 'Cell_ID'})



    # umap.columns

    umap = umap.rename(columns={'Unnamed: 0': 'Cell_ID'})  # 更改umap的列名统一相同的列名Cell ID

    pd.DataFrame(np.isin(umap["Cell_ID"], adata_index["Cell_ID"])).value_counts()

    # intersect = pd.merge(adata_index, umap, on='Cell_ID', how='inner')  # find the overlap Cell_ID between adata_index and umap

    # umap = umap[np.isin(umap["Cell_ID"], adata_index["Cell_ID"])]  # TODO no intersection, remove the suffix fo the adata_index

    umap = umap.drop_duplicates(subset=["Cell_ID"])  # 去除重复值
    umap_ordered = adata_index.merge(umap, on="Cell_ID")  # 依据adata_index Cell ID顺序与umap的数据进行合并

    umap_ordered = umap_ordered.iloc[:, 1:]  # unmap_ordered空的数组

    adata.obsm[['umap_1', 'umap_2']] = umap_ordered.values  # TODO the shape of the adata is not same

    cell_clusters = cell_clusters.iloc[:, 1:]

    cell_clusters = cell_clusters.rename(columns={'cell': 'Cell_ID'})

    cell_clusters = cell_clusters[np.isin(cell_clusters["Cell_ID"], adata_index["Cell_ID"])]
    cell_clusters = cell_clusters.drop_duplicates(subset=["Cell_ID"])  # 去除重复值
    cell_clusters_ordered = adata_index.merge(cell_clusters, on="Cell_ID")
    cell_clusters_ordered = cell_clusters_ordered.iloc[:, 1:]  ####
    adata.obs['clusters'] = cell_clusters_ordered.values

    scv.pp.filter_and_normalize(adata)
    scv.pp.moments(adata)  # 出现了warning
    scv.tl.velocity(adata, mode="stochastic")
    scv.tl.velocity_graph(adata)

    ###spliced/unspliced的比例
    scv.pl.proportions(adata)
    # 可视化
    scv.pl.velocity_embedding(adata, basis='umap')



    print('========================Modify===========================')

    adata_index = pd.DataFrame(adata_index[adata_index.columns[0]].str.split('-', expand=True)[0])
    adata_index = adata_index.rename(columns={adata_index.columns[0]: 'Cell_ID'})

    umap = umap.rename(columns={umap.columns[0]: 'Cell_ID'})

    pd.DataFrame(np.isin(umap["Cell_ID"], adata_index["Cell_ID"])).value_counts()

    adata_index.duplicated().value_counts()  # no duplicated Cell_ID
    umap[umap.columns[0]].duplicated().value_counts()  # no duplicated Cell_ID
    lj = pd.merge(adata_index, umap, on='Cell_ID', how='left')

    lj = lj.iloc[:, 1:]

    adata.obsm['umap'] = lj.values

    cell_clusters = pd.merge(adata_index, cell_clusters, on='Cell_ID', how='left')
    cell_clusters = cell_clusters.iloc[:, 1:]
    adata.obs['clusters'] = cell_clusters.values

    scv.pp.filter_and_normalize(adata)

    scv.pp.filter_and_normalize(adata)
    scv.pp.moments(adata)  # 出现了warning
    scv.tl.velocity(adata, mode="stochastic")
    scv.tl.velocity_graph(adata)

    ###spliced/unspliced的比例
    scv.pl.proportions(adata)
    # 可视化
    scv.pl.velocity_embedding(adata, basis='umap')

    scv.pp.filter_and_normalize(adata)

    scv.logging.print_version()

    adata1 = scv.datasets.pancreas()