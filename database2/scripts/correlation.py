# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/13 18:49
# FileName: correlation
# Description:


import os
import argparse
import numpy as np
import pandas as pd
from scipy import stats

parser = argparse.ArgumentParser(description='scripts to calculate correaltion between frequency and tpm')

parser.add_argument('--frequency', '-f',
                    dest='frequency',
                    metavar='frequency',
                    help='The frequency of the RNA edit sites')

parser.add_argument('--tpm', '-t', dest='tpm',
                    metavar='tpm',
                    help='The tpm of the genes contains RNA edit sites')

parser.add_argument('--output', '-o',
                    dest='output', metavar='path',
                    required=True, default='~/projects/upload/database/sites',
                    help='where to save the final file')
args = parser.parse_args()
freq = args.frequency
tpm = args.tpm
output = args.output


def freqTpmCorrelation(freq: str, tpm: str):
    """

    :param freq:
    :param tpm:
    :return:
    """
    tpm = pd.read_csv(tpm, sep='\t', header=0, low_memory=False)
    freq = pd.read_csv(freq, sep='\t', header=0, low_memory=False)

    array = np.array([])
    for ind, row in freq.iterrows():
        if len(row[9:]) - row[9:].isna().sum() >= 5:
            df1 = pd.DataFrame(freq.iloc[ind, 9:])
            df1 = df1.rename(columns={df1.columns[0]: 'freq'})
            mask = df1.iloc[:, 0].isna()
            df1 = df1.loc[mask == False, ['freq']]

            df2 = pd.DataFrame(tpm.loc[ind, df1.index])
            df2 = df2.rename(columns={df2.columns[0]: 'tpm'})

            array = np.append(array, stats.spearmanr(df1, df2))
            array = np.append(array, len(row[9:]) - row[9:].isna().sum())
        else:
            array = np.append(array, (np.nan, np.nan, np.nan))
    array = array.reshape(-1, 3)
    df = pd.DataFrame(array, columns=['correlation', 'pvalue', 'samples'])
    df = pd.concat([freq.iloc[:, 0:9], df], axis=1)
    return df


if __name__ == '__main__':
    df = freqTpmCorrelation(freq, tpm)
    df.to_csv('%s/%s_correlation.txt' % (output, freq.split('/')[-1].split('.')[0]), sep='\t', index=None)
