import math

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

        self.VARy = self.VARyl[0] + 0.99
        # Need to build index for dictionary
        varNodeKeys = list(self.allvarnode[self.key])

        node_xcv = []
        node_ycv = []
        for i in range(0, len(varNodeKeys)):
            if 'REF' in self.allvarnode[self.key][varNodeKeys[i]]['label'].split()[2]:
                self.allvarnode[self.key][varNodeKeys[i]]['y'] = int(self.REFy)
            else:
                self.allvarnode[self.key][varNodeKeys[i]]['y'] = int(self.VARy)
                node_ycv.append(int(self.VARy))
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
