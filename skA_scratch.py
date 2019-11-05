#### scikit-allel
import allel
import subprocess
import collections
import pandas as pd
import numpy as np
import os

vcfdata = allel.read_vcf("/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Testing/VCFs/INPUT.vcf", fields=['samples','calldata/GT','variants/ALT','variants/REF','variants/CHROM', 'variants/POS', 'variants/svlen'])
vcfdf = allel.vcf_to_dataframe("/mnt/9e6ae416-938b-4e9a-998e-f2c5b22032d2/PD/Workspace/Testing/VCFs/INPUT.vcf", exclude_fields=['QUAL','FILTER_PASS', 'ID'])
sample_set = list(collections.OrderedDict.fromkeys(vcfdata['samples']))
gt = allel.GenotypeArray(vcfdata['calldata/GT']).to_n_alt() # drop additional information
gt_data = pd.DataFrame(gt, columns=sample_set)
dat = pd.concat([vcfdf, gt_data], axis=1, join='inner')
#set(vcfdata['variants/CHROM'])

#check for duplicated values
#vcfdf[vcfdf.duplicated(subset='POS', keep='first')]

regiondata = dat[dat['CHROM'] == 'chrXIV']
regiondata = regiondata[1:2000].reset_index(drop=True)

## We have to add anchors to define
regiondata.loc[-1] = ['chrXIV',0,'','','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]# adding a row
regiondata.index = regiondata.index + 1  # shifting index
regiondata = regiondata.sort_index()
regiondata.loc[len(regiondata)] = ['chrXIV',regiondata.iloc[len(regiondata)-1][1] + 1,'','','','',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#testdat = regiondata[0:20]
#dffrom = regiondata.iloc[::2][["POS","REF"]].reset_index(drop=True)
#dffrom.columns = ["POSfrom","REFfrom"]
#dfto = regiondata.iloc[1::2][["POS","REF"]].reset_index(drop=True)
#dffrom.columns = ["POSto","REFto"]
#refpath = pd.concat([dffrom,dfto ], axis=1)
#refpath.columns = ["POSfrom","REFfrom", "POSto","REFto"]


## Draw graph
from graphviz import Digraph
dot = Digraph(name="Reference",comment='TestGraph', graph_attr={'splines': 'spline', 'rankdir': 'LR'})

fromnode = ""
tonode = ""

for i in range(len(regiondata) - 1):
    fromnode = str(int(regiondata["POS"][i]))
    tonode = str(int(regiondata["POS"][i+1]))

    if fromnode == tonode:
        i = i + 1
    else :
        dot.node(fromnode, label= fromnode)
        dot.node(tonode, label= tonode)
        dot.edge(fromnode, tonode,label="")


#dot.node(str(refpath["POSfrom"][len(refpath) - 1]), label=str(refpath["POSfrom"][len(refpath) - 1]) + " " + str(refpath["REFfrom"][len(refpath) - 1]))
#dot.node(str(refpath["POSto"][len(refpath) - 1]), label=str(refpath["POSto"][len(refpath) - 1]) + " " + str(refpath["REFto"][len(refpath) - 1]))
#dot.edge(str(refpath["POSfrom"][len(refpath) - 1]), str(refpath["POSto"][len(refpath) - 1]),label='')

#dot.view()

## Variant
variant = regiondata[["POS","Y12","ALT_1","ALT_2","ALT_3"]]
variant = variant[variant["Y12"] > 0].reset_index(drop=True)

#testdat = regiondata[0:20]
#vdffrom = regiondata.iloc[::2][["POS","REF"]].reset_index(drop=True)
#dffrom.columns = ["POSfrom","REFfrom"]
#vdfto = regiondata.iloc[1::2][["POS","REF"]].reset_index(drop=True)
#varpath = pd.concat([dffrom,dfto ], axis=1)
#varpath.columns = ["POSfrom","REFfrom", "POSto","REFto"]

#regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][0]][0]-1]

dotx = Digraph(name='YI12', graph_attr={'splines': 'spline', 'rankdir': 'LR'})
fromnode = ""
tonode = ""
integratenode = ""
for i in range(1,len(variant) - 1):
    fromnode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] -1 ][1]))
    tonode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0]][1]))+" "+str(variant["ALT_1"][i])
    integratenode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] +1 ][1]))
    dotx.node(tonode, label = tonode)
    dotx.edge(fromnode, tonode, label="Y12")
    dotx.edge(tonode, integratenode, label="Y12")

dot.subgraph(dotx)

variant = regiondata[["POS","Y55","ALT_1","ALT_2","ALT_3"]]
variant = variant[variant["Y55"] > 0].reset_index(drop=True)
dotx = Digraph(name='Y55', graph_attr={'splines': 'spline', 'rankdir': 'LR'})
fromnode = ""
tonode = ""
integratenode = ""
for i in range(1,len(variant) - 1):
    fromnode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] -1 ][1]))
    tonode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0]][1]))+" "+str(variant["ALT_1"][i])
    integratenode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] +1 ][1]))
    dotx.node(tonode, label = tonode)
    dotx.edge(fromnode, tonode, label="Y55")
    dotx.edge(tonode, integratenode, label="Y55")

dot.subgraph(dotx)

variant = regiondata[["POS","71","ALT_1","ALT_2","ALT_3"]]
variant = variant[variant["71"] > 0].reset_index(drop=True)
dotx = Digraph(name='71', graph_attr={'splines': 'spline', 'rankdir': 'LR'})
fromnode = ""
tonode = ""
integratenode = ""
for i in range(1,len(variant) - 1):
    fromnode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] -1 ][1]))
    tonode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0]][1]))+" "+str(variant["ALT_1"][i])
    integratenode = str(int(regiondata.loc[regiondata.index[regiondata['POS'] == variant['POS'][i]][0] +1 ][1]))
    dotx.node(tonode, label = tonode)
    dotx.edge(fromnode, tonode, label="71")
    dotx.edge(tonode, integratenode, label="71")

dot.subgraph(dotx)

dot.save("scioutput.dot")
#dot.view()

## testing
#str(refpath.loc[refpath.index[refpath['POSfrom'] == variant['POS'][i]]-1])


#pandas plot
import matplotlib.pyplot as plt

#df = regiondata.copy(deep = True)
#df1 = df.loc[df['Y55'] > 0, 'Y55'] = df.loc[df['Y55'] > 0, 'POS']
#df2 = df.loc[df['Y12'] > 0, 'Y12'] = df.loc[df['Y12'] > 0, 'POS']
#df1 = pd.DataFrame(data = df1)
#df1['Y1'] = 1
#df2 = pd.DataFrame(data = df2)
#df2['Y2'] = 2

#select.plot(kind='scatter',x='POS',y='Y55',color='red')

# OR
#ax = plt.gca()

#df1.plot(kind='scatter',x='POS',y='Y1',ax=ax)
#df2.plot(kind='scatter',x='POS',y='Y2', color='red', ax=ax)

#plt.show()

## PLOTLY
import plotly.graph_objs as go

#layout = go.Layout(yaxis=dict(range=[scaleYmin, scaleYmax]), xaxis=dict(range=[0, 500]))
#fig = go.Figure(layout=layout)
fig = go.Figure()

regiondata['REFy'] = 0

with open('/home/rndw/Github/DyeDot/DyeDotOutput/DDbackup.pickle', 'rb') as resumeFile:
    objsToWrite = pickle.load(resumeFile)

xlabs = [regiondata['REF']]
#        fig.add_trace(go.Scatter(
#            x=regiondata['POS'], y=regiondata['REFy'],
#            line=dict(width=0.5, color='grey'),
            # hoverinfo='none',
#            hoverinfo=['all'],
#            mode='lines',
#            name='REFERENCE',
#            text=xlabs
#        ))

        fig.add_trace(go.Scatter(
            x=regiondata['POS'], y=regiondata['REFy'],
            mode='markers',
            hoverinfo='all',
            # hoverinfo='none',
            marker=dict(size=6, line=dict(width=1, color='DarkSlateGrey'), color='grey'),
            line_width=1,
            text=xlabs,
            name='REFERENCE'
        ))

    fig.add_trace(go.Scatter(
        x=edge_xc, y=edge_yc,
        line=dict(width=0.5, color='#888'),
        #hoverinfo='none',
        hoverinfo=['all'],
        mode='lines',
        name='REFERENCE',
        text=xlabs
        )

fig.add_trace(go.Scatter(
    x=df1['POS'], y=df1['Y1'],
    mode='markers',
    hoverinfo='all',
    # hoverinfo='none',
    marker=dict(size=6, line=dict(width=1, color='orange'), color='purple'),
    line_width=1,
    text='Y55',
    name='Y55'
))

fig.add_trace(go.Scatter(
    x=df2['POS'], y=df2['Y2'],
    mode='markers',
    hoverinfo='all',
    # hoverinfo='none',
    marker=dict(size=6, line=dict(width=1, color='green'), color='blue'),
    line_width=1,
    text='Y12',
    name='Y12'
))

fig.write_html('DyeDot_int_output.html')