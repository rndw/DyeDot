import math
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import plotly.plotly as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

class PrepPlotData:

    def __init__(self, refedgedata, refnodedata, allvarnode, allvaredge):
        self.refedgedata = refedgedata
        self.refnodedata = refnodedata
        self.allvarnode = allvarnode
        self.allvaredge = allvaredge

        self.REFy = math.ceil((len(self.allvarnode.keys()) + 1) / 2)
        self.refNodeKeys = list(self.refnodedata.keys())
        self.refEdgeKeys = list(self.refedgedata.keys())

        self.VARyl = list(range(1, len(self.allvarnode.keys()) + 2))
        self.VARyl.pop(self.REFy)

    def RefPrepIGData(self):
        node_xc = []
        node_yc = []
        for i in range(0, len(self.refNodeKeys)):
            self.refnodedata[self.refNodeKeys[i]]['y'] = int(self.REFy)
            self.refnodedata[self.refNodeKeys[i]]['x'] = self.refnodedata[self.refNodeKeys[i]]['label'].split()[1]
            node_xc.append(int(self.refnodedata[self.refNodeKeys[i]]['label'].split()[1]))
            node_yc.append(int(self.REFy))
        edge_xc = []
        edge_yc = []
        for i in range(0, len(self.refedgedata)):
            # From node
            edge_xc.append(int(self.refEdgeKeys[i].split()[0]))
            # To node
            edge_xc.append(int(self.refedgedata[self.refEdgeKeys[i]]['To'].split()[0]))
            # Limiter
            edge_xc.append(None)
            # Need for loop over here - using simple REFy for reference
            edge_yc.append(int(self.REFy))
            edge_yc.append(int(self.REFy))
            edge_yc.append(None)

        return node_xc, node_yc, edge_xc, edge_yc, self.VARyl, self.REFy

    def VarPrepIGData(self, key, VARyl):
        self.key = key
        self.VARyl = VARyl
        #if self.VARyl[0] < self.REFy:
        #    self.VARy = self.REFy - (self.REFy - self.VARyl[0]) * 0.01
        VARy = self.VARyl[0] + 0.99
        #if self.VARyl[0] > self.REFy:
        #    self.VARy = self.REFy + (self.REFy - self.VARyl[0]) * 0.01
        # Need to build index for dictionary
        varNodeKeys = list(self.allvarnode[self.key])

        node_xcv = []
        node_ycv = []
        for i in range(0, len(varNodeKeys)):
            if 'REF' in self.allvarnode[self.key][varNodeKeys[i]]['label'].split()[2]:
                self.allvarnode[self.key][varNodeKeys[i]]['y'] = int(self.REFy)
            else:
                self.allvarnode[self.key][varNodeKeys[i]]['y'] = int(VARy)
                node_ycv.append(int(VARy))
                node_xcv.append(int(self.allvarnode[self.key][varNodeKeys[i]]['label'].split()[1]))

            self.allvarnode[self.key][varNodeKeys[i]]['x'] = int(self.allvarnode[self.key][varNodeKeys[i]]['label'].split()[1])

        # add edges
        # create dict index
        #varEdgeKeys = list(allvaredge[self.key])

        edge_xcv = []
        edge_ycv = []

        for i in range(0, len(varNodeKeys) - 1):
            edge_xcv.append(int(self.allvarnode[self.key][varNodeKeys[i]]['x']))
            edge_ycv.append(int(self.allvarnode[self.key][varNodeKeys[i]]['y']))
            edge_xcv.append(int(self.allvarnode[self.key][varNodeKeys[i + 1]]['x']))
            edge_ycv.append(int(self.allvarnode[self.key][varNodeKeys[i + 1]]['y']))
            edge_xcv.append(None)
            edge_ycv.append(None)

        return node_xcv, node_ycv, edge_xcv, edge_ycv

class PPlot:
    def __init__(self, node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig):
        self.node_xc = node_xc
        self.node_yc = node_yc
        self.allvarnode = allvarnode
        self.edge_xc = edge_xc
        self.edge_yc = edge_yc
        self.refnodedata = refnodedata
        self.fig = fig

    def RefBase(self):

        xlabs = [self.refnodedata[_]['label'] for _ in self.refnodedata.keys()]
        self.fig.add_trace(go.Scattergl(
            x=self.edge_xc, y=self.edge_yc,
            line=dict(width=0.5, color='#888'),
            # hoverinfo='none',
            hoverinfo=['all'],
            mode='lines',
            name='REFERENCE',
            text=xlabs
        ))

        self.fig.add_trace(go.Scattergl(
            x=self.node_xc, y=self.node_yc,
            mode='markers',
            hoverinfo='all',
            # hoverinfo='none',
            marker=dict(size=12, line=dict(width=2, color='DarkSlateGrey')),
            line_width=2,
            text=xlabs,
            name='REFERENCE'
        ))

        return self.fig

    def VarG(self,xlabs, key):
        self.xlabs = xlabs
        self.key = key

        self.fig.add_trace(go.Scattergl(
            x=self.edge_xc, y=self.edge_yc,
            line=dict(width=2, color='red'),
            hoverinfo='all',
            mode='lines',
            name=self.key,
            text=self.xlabs
        ))

        self.fig.add_trace(go.Scattergl(
            x=self.node_xc, y=self.node_yc,
            mode='markers',
            hoverinfo='all',
            # hoverinfo='none',
            # marker=dict(size=10,line=dict(width=2,color='blue'), symbol = 'square'),
            marker=dict(size=10, line=dict(width=2, color='blue')),
            line_width=2,
            text=self.xlabs,
            name=self.key
        ))


        return self.fig