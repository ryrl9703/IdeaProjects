# -*- encoding: utf-8 -*-
"""
@Introduce  :
@File       : pyscenicTutorial.py
@Author     : ryrl
@email      : 18762739367@163.com
@Time       : 2022/8/26 21:52
"""

import os
import glob
import pickle
import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from dask.diagnostics import ProgressBar

from arboreto.utils import load_tf_names
from arboreto.algo import grnboost2

from ctxcore.rnkdb import FeatherRankingDatabase as RankingDatabase
from pyscenic.utils import modules_from_adjacencies, load_motifs
from pyscenic.prune import prune2df, df2regulons
from pyscenic.aucell import aucell

from modules.utils import name

parser = argparse.ArgumentParser(description='scripts to run pyscenic')

parser.add_argument('--expression', '-e',
                    dest='exp',
                    metavar='single cell expression matrix',
                    required=True,
                    help='The the Single Cell expression matrix, split by tab')

parser.add_argument('--database', '-b',
                    dest='dbs',
                    metavar='database file',
                    required=True,
                    help='The path of the the cisTargets database file, eg: *ranking.feather')

parser.add_argument('--mfile1', '-m1',
                    dest='mf1',
                    metavar='motif listed file',
                    required=True,
                    help='The file that list TFs')

parser.add_argument('--resources', '-r',
                    dest='res',
                    metavar='resources file',
                    required=True,
                    help='The motif annotation file name, eg: *.tbl')

parser.add_argument('--mfile2', '-t2',
                    dest='mf2',
                    metavar='motif file',
                    required=True,
                    help='The path and file name to save the motif enrichment results')

parser.add_argument('--gfile', '-g',
                    dest='reg',
                    metavar='regulons file',
                    required=True,
                    help='The path and file name to save the regulons results')


args = parser.parse_args()
mat = args.exp
mf1 = args.mf1
dbs = args.dbs
res = args.res
mf2 = args.mf2
reg = args.reg


if __name__ == '__main__':
    exp = pd.read_csv(mat, sep='\t', header=0, index_col=0).T
    tfs = load_tf_names(mf1)

    db_fnames = glob.glob(dbs)

    dbs = [RankingDatabase(fname=fname, name=name(fname)) for fname in db_fnames]
    adjacencies = grnboost2(expression_data=exp, tf_names=tfs, verbose=True)

    """
    Regulons are drived from adjacencies based on three mrthods:
        1、create the TF-modules is to select the best targets for each transcription factor:
            1) Targets with importance > the 50th percentile
            2) Targets with importance > the 75th percentile
            3) Targets with importance > the 90th percentile
        
        2、The second method is to select the top target for a given TF:
            Top 50 targets(targets with highest weight)
            
        3、 select the best regulators for each gene(this is actually how GENIE3 internally works).
            Then, these targets can be assigned back to each TF to form the TF-modules.
            1) Targets for which the TF is within its top5 regulators
            2) Targets for which the TF is within its top10 regulators
            3) Targets for which the TF is within its top50 regulators
    """
    modules = list(modules_from_adjacencies(adjacencies=adjacencies, ex_mtx=exp))

    # Calculate a list of enriched motifs and the corresponding target genes for all modules.
    with ProgressBar():
        df = prune2df(dbs, modules=modules, motif_annotations_fname=res)

    # Create regulons from this table of enriched motifs.
    regulons = df2regulons(df=df)

    # Save the enriched motifs and the discovered regulons to disk.
    df.to_csv(os.path.join(mf2, 'motifs_enrichment.csv'))

    with open(os.path.join(reg, 'regulons.p', 'wb')) as f:
        pickle.dump(regulons, f)

    # The clusters can be everaged via the dask framework:
    df = prune2df(rnkdbs=dbs, modules=modules, motif_annotations_fname=res, num_workers=20)

    # Reloading the enriched motifs and regulons from file should be done as follows
    df1 = load_motifs(fname=os.path.join(mf2, 'motifs_enrichment.csv'), sep=',')

    with open(os.path.join(reg, 'regulons.p', 'wb'), 'rb') as f:
        regulons = pickle.load(f)

    """
    We characterized the different cells in a single-cell transcriptomics expriment via the enrichment of the previously
    discovered regulons. Enrichment of a regulon is measured as the Area Under the recovery Curve(AUC) of the genes that
    define this regulon
    """

    auc_mtx = aucell(exp, regulons, num_workers=20)
    sns.clustermap(auc_mtx, figsize=(8, 8))
    plt.show()
