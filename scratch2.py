## compare our vcf parser with scikit-allel and plink
from os import name
import os
from time import time
import argparse
from class_vcf_parser import ReadVcfs, VarGraphCons, RegionOfInterestGraph, VariantList
from class_Grapher import RefGraphBuilder
from class_Utils import DataUtils
import math
from class_PlotIG import PrepPlotData

import allel


# 37.0 MB vcf
path = "/home/rndw/Github/DyeDot/VCF/Single/DBVPG6044.vcf"
# 1.3 GB
path = "/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Alexa_VCF/denovo.Africa_Chr6.final_filtered_var_pca.vcf"

start = time()
callset = allel.read_vcf(path)
print(time() - start)

path = "/home/rndw/Github/DyeDot/VCF/Single/"
path = "/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Alexa_VCF/"

start = time()
#dat_test = ReadVcfs(path).variant_builder()
test_out = VariantList(path, filename="denovo.Africa_Chr6.final_filtered_var_pca.vcf", sample="denovo.Africa_Chr6.final_filtered_var_pca").vcf_reader()
#output_test = VarGraphCons().anchor_builder(dat_test, path)
print(time() - start)

sys.getsizeof(test_out)
sys.getsizeof(callset)

### Doesn't work
#from pprint import pprint
#from pdbio.vcfdataframe import VcfDataFrame

#path = "/home/rndw/Github/DyeDot/VCF/Single/DBVPG6044.vcf"
#start = time()
#vcfdf = VcfDataFrame(path=path)
#print(time() - start)

import vcf
import pandas as pd
import numpy as np
reader = vcf.Reader(open(path, 'r'))
start = time()
n = 0
df = {}
for line in reader:
    linedat = {
        'CHROM': line.CHROM,
        'POS': line.POS,
        'REF': line.REF,
        'ALT': tuple(line.ALT)
    }
    for sample, call in zip(reader.samples, line.samples):
        datum = dict(linedat)
        datum['sample'] = sample
        datum.update(zip(call.data._fields, call.data))
        df[n] = datum
        n = n+1

data = pd.DataFrame.from_dict(df, orient='index')
data = data.set_index(['CHROM', 'POS', 'REF', 'sample'])
print(time() - start)


