
## quick run start
from os import name
import os
from time import time
import argparse
from class_vcf_parser import ReadVcfs, VarGraphCons, RegionOfInterestGraph
from class_Grapher import RefGraphBuilder
from class_Utils import DataUtils
import math
from class_PlotIG import PrepPlotData


outDir = os.getcwd() + "/DyeDotOutput"
try:
    os.mkdir(outDir)
except FileExistsError:
    print("Directory exists, files will be overwritten!")
    pass
finally:
    print(f"Output directory: {outDir}")

loci = ['chrI',0,50000]
loci = ['chrI', 0, 1050000]
#path = '/home/rndw/Github/RefGraph/Dyedot_variationGraphs/Small_vcfs/'
path = '/home/rndw/Github/DyeDot/VCF/genome_multi/'
#path = '/mnt/Data/PD/Workspace/Testing/VCFs/'
#path = '/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Testing/VCFs/'
dat = ReadVcfs(path).variant_builder()

## Have a look at scikit-allel
#import scikit-allel
output = VarGraphCons().anchor_builder(dat, path)
# LIMIT DATA TO SPECIFIED REGION
# IMPROVEMENT: OUTPUT MULTIPLE RANGES OR BLOCKS

import pickle
pickle_data = [loci, path, dat, output]
pickle.dump(pickle_data, open( "test_bck.pkl", "wb" ))

loci, path, dat, output = pickle.load(open("test_bck.pkl", "rb"))

RegionOfInterestGraph(output, loci).region()
# CONSTRUCT A REFERENCE PATH OBJECT. THIS COULD BE ANYTHING REALLY (HAPLOTYPES) - AS LONG AS IT CONTAINS OVERLAPPING NODES
refpath = RegionOfInterestGraph(output, loci).referencegr()

# CONSTRUCT THE REFERENCE PATH
graph, refnodedata, refedgedata = RefGraphBuilder(refpath=refpath).referencepath()

# CONSTRUCT THE VARAINT PATHS: BUILT ON TOP OF THE REFERENCE PATH
xgraph, varnodedata, varedgedata, allvarnode, allvaredge = RefGraphBuilder(refpath=refpath).variantpath(output, graph,loci, refpath)

# Write objects to disk to resume
# This would work better as a dictionary - why did I make it a list? - DONE
objsToWrite = {'refnodedata': refnodedata, 'refedgedata': refedgedata, 'varnodedata': varnodedata,
               'varedgedata': varedgedata, 'allvarnode': allvarnode, 'allvaredge': allvaredge}
graphObjs = {'graph': graph, 'xgraph': xgraph}
DataUtils().resumeBck(objsToWrite=objsToWrite, graphObjs=graphObjs, outDir=outDir)

#### test writing
    with open('yi38_nodes.txt', 'w') as f:
        # f.writelines(str(objsToWrite[item]))  # can only write strings, not dictionaries
        f.writelines('{}:{}\n'.format(k, v) for k, v in allvarnode['yi38small'].items())

#newobjstowrite = dataUtils().resumeFromBck(bckPath=outDir)

#### Testings

# y position
REFy = math.ceil((len(objsToWrite['allvarnode'].keys()) + 1) / 2)
# Need to build index for dictionary
refKeys = list(refnodedata.keys())
for i in range(0,len(refKeys)):
    refnodedata[refKeys[i]]['y'] = REFy
    refnodedata[refKeys[i]]['x'] = int(refnodedata[refKeys[i]]['label'].split()[1])

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot



##############################done

#### refernence
xlabs = [refnodedata[_]['label'] for _ in refnodedata.keys()]
fig.add_trace(go.Scattergl(
    x=edge_xc, y=edge_yc,
    line=dict(width=0.5, color='#888'),
    #hoverinfo='none',
    hoverinfo=['all'],
    mode='lines',
    name='REFERENCE',
    text=xlabs
    ))

fig.add_trace(go.Scattergl(
    x=node_xc, y=node_yc,
    mode='markers',
    hoverinfo='all',
    #hoverinfo='none',
    #marker=dict(size=10,line=dict(width=2,color='DarkSlateGrey'), symbol = 'square'),
marker=dict(size=10,line=dict(width=2,color='DarkSlateGrey')),
    line_width=2,
    text=xlabs,
    name='REFERENCE'
    ))
#####

xlabs = [allvarnode['yi38small'][_]['label'] for _ in allvarnode['yi38small'].keys()]
fig.add_trace(go.Scattergl(
    x=edge_xcv, y=edge_ycv,
    line=dict(width=2, color='red'),
    hoverinfo='all',
    mode='lines',
    name='YI38',
    text=xlabs
    ))

fig.add_trace(go.Scattergl(
    x=node_xcv, y=node_ycv,
    mode='markers',
    hoverinfo='all',
    #hoverinfo='none',
    #marker=dict(size=10,line=dict(width=2,color='blue'), symbol = 'square'),
marker=dict(size=10,line=dict(width=2,color='blue')),
    line_width=2,
    text=xlabs,
    name='YI38'
    ))

fig.layout.update(title=go.layout.Title(text='Chromosome', xref='paper', x=0), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Coordinates')))

# manual plotting of boxes
#fig.layout.update(shapes=nodeShapes)

# comment out to allow CI pass
# plot(fig, filename= str(outDir + '/' + 'DyeDot_int_output.html'))
# Save locally
fig.write_html(str(outDir + '/' + 'DyeDot_int_output.html'))


#### y slider mode
from class_PlotIG import PrepPlotData, PPlot
scaleYmin = (len(allvarnode.keys())/2) - 2
scaleYmax = (len(allvarnode.keys())/2) + 2
node_xc, node_yc, edge_xc, edge_yc, VARyl, REFy = PrepPlotData(refedgedata, refnodedata, allvarnode, allvaredge).RefPrepIGData()

import plotly.graph_objs as go

layout = go.Layout(yaxis=dict(range=[scaleYmin, scaleYmax]), xaxis=dict(range=[0, 500]))
fig = go.Figure(layout=layout)

#from ipywidgets import interactive, HBox, VBox, widgets, interact

fig = PPlot(node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig).RefBase()


for key in list(allvarnode.keys()):
    VARy = PrepPlotData(refedgedata, refnodedata, allvarnode, allvaredge).yScaler(VARyl)
    node_xc, node_yc, edge_xc, edge_yc = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).VarPrepIGData(key, VARy)
    VARyl.remove(VARyl[0])
    xlabs = [allvarnode[key][_]['label'] for _ in allvarnode[key].keys()]
    fig = PPlot(node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig).VarG(xlabs, key)



fig.layout.update(title=go.layout.Title(text='Chromosome', xref='paper', x=0), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Coordinates')), xaxis_rangeslider_visible=True)
fig.write_html(str(outDir + '/' + 'DyeDot_int_output.html'))



<<<<<<< HEAD



### GLOBAL GENOME plot############################################
from class_PlotIG import PrepPlotData, PPlot
import plotly.graph_objs as go

# y position
REFy = math.ceil((len(objsToWrite['allvarnode'].keys()) + 1) / 2)
# Need to build index for dictionary
refKeys = list(refnodedata.keys())
for i in range(0,len(refKeys)):
    refnodedata[refKeys[i]]['y'] = REFy
    refnodedata[refKeys[i]]['x'] = int(refnodedata[refKeys[i]]['label'].split()[1])

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot



#chroms = ['chrI','chrII','chrIII','chrIV','chrV','chrVI','chrVII','chrVIII','chrIX','chrX','chrXI','chrXII','chrXIII','chrXIV','chrXV','chrXVI','chrM']
chroms = ['chrI','chrII','chrIII']
fig = plotly.tools.make_subplots(rows=3,cols=1)

for i in chroms:
    loci = [i, 0, 12000000]
    dat = ReadVcfs(path).variant_builder()

    output = VarGraphCons().anchor_builder(dat, path)
    RegionOfInterestGraph(output, loci).region()
    refpath = RegionOfInterestGraph(output, loci).referencegr()
    graph, refnodedata, refedgedata = RefGraphBuilder(refpath=refpath).referencepath()
    xgraph, varnodedata, varedgedata, allvarnode, allvaredge = RefGraphBuilder(refpath=refpath).variantpath(output,graph, loci,refpath)

    node_xc, node_yc, edge_xc, edge_yc, VARyl, REFy = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).RefPrepIGData()

    xlabs = [refnodedata[_]['label'] for _ in refnodedata.keys()]
    trace1 = go.Scattergl(
        x=edge_xc, y=edge_yc,
        line=dict(width=0.5, color='#888'),
        #hoverinfo='none',
        hoverinfo=['all'],
        mode='lines',
        name='REFERENCE',
        text=xlabs
        )

    trace2 = go.Scattergl(
        x=node_xc, y=node_yc,
        mode='markers',
        hoverinfo='all',
        #hoverinfo='none',
        #marker=dict(size=10,line=dict(width=2,color='DarkSlateGrey'), symbol = 'square'),
    marker=dict(size=10,line=dict(width=2,color='DarkSlateGrey')),
        line_width=2,
        #text=xlabs,
        name='REFERENCE'
        )

    key = 'YI38P'
        VARy = PrepPlotData(refedgedata, refnodedata, allvarnode, allvaredge).yScaler(VARyl)
        node_xcv, node_ycv, edge_xcv, edge_ycv = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).VarPrepIGData(key, VARy)
        VARyl.remove(VARyl[0])
        xlabs = [allvarnode[key][_]['label'] for _ in allvarnode[key].keys()]


    trace3 = go.Scattergl(
        x=edge_xcv, y=edge_ycv,
        line=dict(width=2, color='red'),
        hoverinfo='all',
        mode='lines',
        #name='YI38',
        #text=xlabs
    )

    trace4 = go.Scattergl(
        x=node_xcv, y=node_ycv,
        mode='markers',
        hoverinfo='all',
        # hoverinfo='none',
        # marker=dict(size=10,line=dict(width=2,color='blue'), symbol = 'square'),
        marker=dict(size=10, line=dict(width=2, color='blue')),
        line_width=2,
        #text=xlabs,
        #name='YI38'
    )

#####



fig.append_trace(trace1,1,1)
fig.append_trace(trace2,1,1)
fig.append_trace(trace3,1,1)
fig.append_trace(trace4,1,1)

fig.append_trace(trace1,2,1)
fig.append_trace(trace2,2,1)
fig.append_trace(trace3,2,1)
fig.append_trace(trace4,2,1)

fig.write_html(str(outDir + '/' + 'DyeDot_int_output_testmulti.html'))

=======
## tkinter
>>>>>>> a9efb66e0ef21d052cb074fd1c981d6f362ed5dc


#### scikit-allel
import allel
import subprocess
import collections
import pandas as pd
import numpy as np

vcfdata = allel.read_vcf("/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Alexa_VCF/denovo.Africa_Chr6.final_filtered_var_pca.vcf", fields=['samples','calldata/GT','variants/ALT','variants/REF','variants/CHROM', 'variants/POS', 'variants/svlen'])
vcfdf = allel.vcf_to_dataframe("/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Alexa_VCF/denovo.Africa_Chr6.final_filtered_var_pca.vcf", exclude_fields=['QUAL','FILTER_PASS', 'ID'])

vcfdata.keys()
set(vcfdata['variants/CHROM'])

regiondata = dat[dat['CHROM'] == 'chr6']

testdat = regiondata[0:20]

refpath = pd.concat([testdat.iloc[::2][["POS","REF"]].reset_index(drop=True), testdat.iloc[1::2][["POS","REF"]].reset_index(drop=True)], axis=1)
