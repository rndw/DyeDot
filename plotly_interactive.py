
# y position
REFy = math.ceil((len(objsToWrite['allvarnode'].keys()) + 1) / 2)
# Need to build index for dictionary
refNodeKeys = list(refnodedata.keys())

node_xc = []
node_yc = []
for i in range(0,len(refNodeKeys)):
    refnodedata[refNodeKeys[i]]['y'] = REFy
    refnodedata[refNodeKeys[i]]['x'] = refnodedata[refNodeKeys[i]]['label'].split()[1]
    node_xc.append(refnodedata[refNodeKeys[i]]['label'].split()[1])
    node_yc.append(REFy)

# add edges
# create dict index
refEdgeKeys = list(refedgedata.keys())

edge_xc = []
edge_yc = []
for i in range(0,len(refedgedata)):
    # need to add y vars
    #refedgedata[refEdgeKeys[i]]['x'] = refEdgedata[refNodeKeys[i]]['label'].split()[1]
    # From node
    edge_xc.append(refEdgeKeys[i].split()[0])
    # To node
    edge_xc.append(refedgedata[refEdgeKeys[i]]['To'].split()[0])
    # Limiter
    edge_xc.append(None)
    # Need for loop over here - using simple REFy for reference
    edge_yc.append(REFy)
    edge_yc.append(REFy)
    edge_yc.append(None)

# ADD VARIANT data
# y position
VARy = 1
# Need to build index for dictionary
varNodeKeys = list(allvarnode['yi38small'])

node_xcv = []
node_ycv = []
for i in range(0,len(varNodeKeys)):
    if 'REF' in allvarnode['yi38small'][varNodeKeys[i]]['label'].split()[2]:
        allvarnode['yi38small'][varNodeKeys[i]]['y'] = REFy
        node_ycv.append(REFy)
    else:
        allvarnode['yi38small'][varNodeKeys[i]]['y'] = VARy
        node_ycv.append(VARy)

    allvarnode['yi38small'][varNodeKeys[i]]['x'] = allvarnode['yi38small'][varNodeKeys[i]]['label'].split()[1]
    node_xcv.append(allvarnode['yi38small'][varNodeKeys[i]]['label'].split()[1])

# add edges
# create dict index
varEdgeKeys = list(allvaredge['yi38small'])


edge_xcv = []
edge_ycv = []

for i in range(0,len(varNodeKeys) - 1):
    edge_xcv.append(allvarnode['yi38small'][varNodeKeys[i]]['x'])
    edge_ycv.append(allvarnode['yi38small'][varNodeKeys[i]]['y'])
    edge_xcv.append(allvarnode['yi38small'][varNodeKeys[i + 1]]['x'])
    edge_ycv.append(allvarnode['yi38small'][varNodeKeys[i + 1]]['y'])
    edge_xcv.append(None)
    edge_ycv.append(None)

# only add non-reference nodes
varNodeKeysUniq = []
node_xcvu = []
node_ycvu = []
for i in range(0,len(varNodeKeys)):
    if not 'REF' in varNodeKeys[i]:
        varNodeKeysUniq.append(varNodeKeys[i])
        node_xcvu.append(allvarnode['yi38small'][varNodeKeys[i]]['x'])
        node_ycvu.append(allvarnode['yi38small'][varNodeKeys[i]]['y'])


######################### mf1
VARy = 3
# Need to build index for dictionary
varNodeKeys = list(allvarnode['mf1small'])

node_xcvm = []
node_ycvm = []
for i in range(0,len(varNodeKeys)):
    if 'REF' in allvarnode['mf1small'][varNodeKeys[i]]['label'].split()[2]:
        allvarnode['mf1small'][varNodeKeys[i]]['y'] = REFy
        node_ycvm.append(REFy)
    else:
        allvarnode['mf1small'][varNodeKeys[i]]['y'] = VARy
        node_ycvm.append(VARy)

    allvarnode['mf1small'][varNodeKeys[i]]['x'] = allvarnode['mf1small'][varNodeKeys[i]]['label'].split()[1]
    node_xcvm.append(allvarnode['mf1small'][varNodeKeys[i]]['label'].split()[1])

# add edges
# create dict index
varEdgeKeys = list(allvaredge['mf1small'])


edge_xcvm = []
edge_ycvm = []

for i in range(0,len(varNodeKeys) - 1):
    edge_xcvm.append(allvarnode['mf1small'][varNodeKeys[i]]['x'])
    edge_ycvm.append(allvarnode['mf1small'][varNodeKeys[i]]['y'])
    edge_xcvm.append(allvarnode['mf1small'][varNodeKeys[i + 1]]['x'])
    edge_ycvm.append(allvarnode['mf1small'][varNodeKeys[i + 1]]['y'])
    edge_xcvm.append(None)
    edge_ycvm.append(None)

# only add non-reference nodes
varNodeKeysUniq = []
node_xcvum = []
node_ycvum = []
for i in range(0,len(varNodeKeys)):
    if not 'REF' in varNodeKeys[i]:
        varNodeKeysUniq.append(varNodeKeys[i])
        node_xcvum.append(allvarnode['mf1small'][varNodeKeys[i]]['x'])
        node_ycvum.append(allvarnode['mf1small'][varNodeKeys[i]]['y'])
        

######################### mf1
VARy = 0
# Need to build index for dictionary
varNodeKeys = list(allvarnode['j11small'])

node_xcvj = []
node_ycvj = []
for i in range(0,len(varNodeKeys)):
    if 'REF' in allvarnode['j11small'][varNodeKeys[i]]['label'].split()[2]:
        allvarnode['j11small'][varNodeKeys[i]]['y'] = REFy
        node_ycvj.append(REFy)
    else:
        allvarnode['j11small'][varNodeKeys[i]]['y'] = VARy
        node_ycvj.append(VARy)

    allvarnode['j11small'][varNodeKeys[i]]['x'] = allvarnode['j11small'][varNodeKeys[i]]['label'].split()[1]
    node_xcvj.append(allvarnode['j11small'][varNodeKeys[i]]['label'].split()[1])

# add edges
# create dict index
varEdgeKeys = list(allvaredge['j11small'])


edge_xcvj = []
edge_ycvj = []

for i in range(0,len(varNodeKeys) - 1):
    edge_xcvj.append(allvarnode['j11small'][varNodeKeys[i]]['x'])
    edge_ycvj.append(allvarnode['j11small'][varNodeKeys[i]]['y'])
    edge_xcvj.append(allvarnode['j11small'][varNodeKeys[i + 1]]['x'])
    edge_ycvj.append(allvarnode['j11small'][varNodeKeys[i + 1]]['y'])
    edge_xcvj.append(None)
    edge_ycvj.append(None)

# only add non-reference nodes
varNodeKeysUniq = []
node_xcvuj = []
node_ycvuj = []
for i in range(0,len(varNodeKeys)):
    if not 'REF' in varNodeKeys[i]:
        varNodeKeysUniq.append(varNodeKeys[i])
        node_xcvuj.append(allvarnode['j11small'][varNodeKeys[i]]['x'])
        node_ycvuj.append(allvarnode['j11small'][varNodeKeys[i]]['y'])

import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

# set the default zoom level
# could ask user for this
# should add dynamic scaling based on input (y axis)
layout = go.Layout(
    yaxis=dict(
        range=[-0.5, 3.5]
    ),
    xaxis=dict(
        range=[0, 500]
    )
)


fig = go.Figure(layout=layout)
# add var edges
fig.add_trace(go.Scatter(
    x=edge_xcv, y=edge_ycv,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=edge_xcvj, y=edge_ycvj,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'))
fig.add_trace(go.Scatter(
    x=edge_xcvm, y=edge_ycvm,
    line=dict(width=2, color='#888'),
    hoverinfo='none',
    mode='lines'))
# add edges
fig.add_trace(go.Scatter(
    x=edge_xc, y=edge_yc,
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines'))
# Add var node trace
fig.add_trace(go.Scatter(
    x=node_xcvuj, y=node_ycvuj,
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


fig.add_trace(go.Scatter(
    x=node_xcvum, y=node_ycvum,
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

fig.add_trace(go.Scatter(
    x=node_xcvu, y=node_ycvu,
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
### basic node trace
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

# This needs to be updated on the fly - just a test at this stage
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


# comment out to allow CI pass
# plot(fig, filename= str(outDir + '/' + 'DyeDot_int_output.html'))
# Save locally
fig.write_html(str(outDir + '/' + 'DyeDot_int_output.html'))