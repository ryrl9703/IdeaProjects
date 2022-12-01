# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/6 13:19
# FileName: rnaAbundances
# Description:


import os
import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='scripts to ')

parser.add_argument('--directory', '-d', dest='directory',
                    metavar='directory',
                    default='/public/workspace/ryrl/projects/rnaedit_autoimmune/data',
                    help='The path to the directory that contains all disease data, default: '
                         '/public/workspace/ryrl/projects/rnaedit_autoimmune/data')

parser.add_argument('--file', '-f', dest='file',
                    metavar='filename', required=True,
                    help='The file name you want to search')

parser.add_argument('--path', '-p', dest='path',
                    metavar='directory',
                    default='/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset',
                    help='The directory store the geneAnnotation, '
                         'default:/public/workspace/ryrl/projects/upload/database/sites/merge_each_dataset')

parser.add_argument('--output', '-o',
                    dest='output', metavar='path',
                    required=True, default='~/projects/upload/database/sites',
                    help='where to save the final file')
args = parser.parse_args()
dirs = args.directory
file = args.file
path = args.path
output = args.output


def find_file(dirs: str, filename: str) -> list:
    """

    :param filename:
    :param dirs:
    :return:
    """
    lst = []
    for root, dirs, files in os.walk(dirs):
        for i in files:
            if i == filename:
                lst.append('%s/%s' % (root, i))
    return lst


if __name__ == '__main__':
    lst = find_file(dirs, file)

    for i in lst:
        dis = i.split('/')[7]
        gse = i.split('/')[8].replace('_', '')

        tpm = pd.read_csv(i, sep='\t', header=0)
        if os.path.exists('%s/%s/%s.contact.txt' % (path, dis, gse)):
            df = pd.read_csv('%s/%s/%s.contact.txt' % (path, dis, gse), sep='\t',
                             header=0)  # .str.split(',').explode().drop_duplicates()
            genes = df['genes']
            index = tpm.index.isin(genes)
            geneEditedTpm = tpm[index]
            geneEditedTpm = pd.merge(df.iloc[:, 0:9], geneEditedTpm,
                                     left_on=['genes'], right_index=True, how='left')
            geneEditedTpm.to_csv('%s/%s_%s_geneEditedTpm.txt' % (output, dis, gse), sep='\t', index=None)
        else:
            print('%s/%s/%s.contact.txt not exit' % (path, dis, gse))
