# coding: utf-8
# Author: ryrl
# CreateTime: 2022/7/4 9:59
# FileName: BamBasesStatics
# Description:

import os
import pybedtools
import pandas as pd


os.chdir('/public/workspace/ryrl/projects/rnaedit_autoimmune/data/SystemicLupusErythematosus/GSE110685')


genome_base = pybedtools.BedTool.genome_coverage('alignment/SRR6730185Aligned.sortedByCoord.out.bam')
genome_base = pybedtools.example_bedtool('../SRR6730185Aligned_sortedByCoord_out.bam')
genome_base.genome_coverage(bg=True)