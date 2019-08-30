class rawData():

    def __init__(self):
        pass

    def nodeData(self, refpath, i, nw, nodedata, key):
        self.refpath = refpath
        self.i = i
        self.nw = nw
        self.nodedata = nodedata
        ## expose key argument for nodes - might need at a later stage
        self.key = key


        nodedata[str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2])] = ["label", str(self.refpath[self.i - 1][0] + ' ' + self.refpath[self.i - 1][1] + ' ' + self.refpath[self.i - 1][2]), "width", str(self.nw)]

        return nodedata

    ## not necessary to add node width (nw)
    def edgeData(self, refpath, i, nw, edgedata, key):
        self.refpath = refpath
        self.i = i
        self.nw = nw
        self.edgedata = edgedata
        self.key = key

        #edgedata.append((str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2]), str(self.refpath[self.i][1] + self.refpath[self.i][2])))
        #edge_attr = {'arrowhead': 'vee', 'arrowsize': '0.5', 'color': 'black', 'penwidth': '2'}

        edgedata[str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2]), str(self.refpath[self.i][1] + self.refpath[self.i][2])] = ["label", self.key]

        return edgedata
