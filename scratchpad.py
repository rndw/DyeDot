nodedata = {}
for i in range(1, len(refpath) - 1):  # Has to start at one, else loopback in graph
    nw = (int(refpath[i + 1][1]) - int(refpath[i][1])) / 10
    if nw < 1.2:
        nw = 1.2

    nodedata[str(refpath[i - 1][1] + refpath[i - 1][2])] = ["label", str(refpath[i - 1][0] + ' ' + refpath[i - 1][1] + ' ' + refpath[i - 1][2]), "width", str(nw)]
    #p.edge(self.refpath[i - 1][1] + self.refpath[i - 1][2], self.refpath[i][1] + self.refpath[i][2])


## quick run start
from os import name
import os
from time import time
import argparse
from class_vcf_parser import ReadVcfs, VarGraphCons, RegionOfInterestGraph
from class_Grapher import RefGraphBuilder
from class_Utils import DataUtils

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
xgraph, varnodedata, varedgedata, allvarnode, allvaredge = RefGraphBuilder(refpath=refpath).variantpath(output, graph,
                                                                                                        loci, refpath)

# Write objects to disk to resume
# This would work better as a dictionary - why did I make it a list? - DONE
objsToWrite = {'refnodedata': refnodedata, 'refedgedata': refedgedata, 'varnodedata': varnodedata,
               'varedgedata': varedgedata, 'allvarnode': allvarnode, 'allvaredge': allvaredge}
graphObjs = {'graph': graph, 'xgraph': xgraph}
DataUtils().resumeBck(objsToWrite=objsToWrite, graphObjs=graphObjs, outDir=outDir)

#newobjstowrite = dataUtils().resumeFromBck(bckPath=outDir)

#### Testings

# y position
REFy = math.ceil((len(objsToWrite['allvarnode'].keys()) + 1) / 2)
# Need to build index for dictionary
refKeys = list(refnodedata.keys())
for i in range(0,len(refKeys)):
    refnodedata[refKeys[i]]['y'] = REFy
    refnodedata[refKeys[i]]['x'] = refnodedata[refKeys[i]]['label'].split()[1]

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#node_adjacencies = []
#node_text = []
#for node, adjacencies in enumerate(g.adjacency()):
#    node_adjacencies.append(len(adjacencies[1]))
#    node_text.append('# of connections: '+str(len(adjacencies[1])))

#node_trace.marker.color = node_adjacencies
#node_trace.text = node_text


### custom
#edge_xc = []
#edge_xc = [1,2,None,2,3,None,1,3,None]
#edge_yc = []
#edge_yc = [1,2,None,2,1,None,1,1,None]

#edge_xcy = []
#edge_xcy = [1,2,None]
#edge_ycy = []
#edge_ycy = [1,2,None]

##############################done
##node_xc = []
##node_xc = [1,2,3]
##node_yc = []
##node_yc = [1,2,1]


fig = go.Figure()

# Add scatter trace for line
fig.add_trace(go.Scatter(
    x=edge_xcy, y=edge_ycy,
    line=dict(width=2, color='#200'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=edge_xc, y=edge_yc,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=node_xc, y=node_yc,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        # colorscale options
        #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
        #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
        #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
        colorscale='YlGnBu',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        ),
        line_width=2)))

fig.layout.update(
    shapes=[
        # 1st highlight during Feb 4 - Feb 6
        go.layout.Shape(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            # y-reference is assigned to the plot paper [0,1]
            yref="paper",
            x0=0.75,
            y0=0.75,
            x1=1.25,
            y1=1.25,
            fillcolor="LightSalmon",
            opacity=0.5,
            layer="below",
            line_width=0,
        ),
    ]
)

plot(fig)