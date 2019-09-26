
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

#loci = ['chrI',0,50000]
loci = ['chrVII', 0, 1050000]
#path = '/home/rndw/Github/RefGraph/Dyedot_variationGraphs/Small_vcfs/'
path = '/home/rndw/Github/DyeDot/VCF/'
#path = '/mnt/Data/PD/Workspace/Testing/VCFs/'
dat = ReadVcfs(path).variant_builder()

output = VarGraphCons().anchor_builder(dat, path)
# LIMIT DATA TO SPECIFIED REGION
# IMPROVEMENT: OUTPUT MULTIPLE RANGES OR BLOCKS
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
#import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#node_adjacencies = []
#node_text = []
#for node, adjacencies in enumerate(g.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))
#    node_text.append('# of connections: '+str(len(adjacencies[1])))

#node_trace.marker.color = node_adjacencies
#node_trace.text = node_text


### custom

##############################done
layout = go.Layout(
    yaxis=dict(
        range=[-0.5, 3.5],
        nticks=3
    ),
    xaxis=dict(
        range=[0, 50],
        nticks=200000000
    )
)


fig = go.Figure(layout=layout)
#fig.update_yaxes(nticks=3)
#fig.update_xaxes(nticks=2000000000)

fig.update_yaxes(tick0=2, dtick=0.5)
fig.update_xaxes(tick0=0, dtick=0.5)



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