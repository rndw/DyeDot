class rawData():

    def __init__(self):
        pass

    def nodeData(self, refpath, i, nw, nodedata):
        self.refpath = refpath
        self.i = i
        self.nw = nw
        self.nodedata = nodedata

        nodedata[str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2])] = ["label", str(self.refpath[self.i - 1][0] + ' ' + self.refpath[self.i - 1][1] + ' ' + self.refpath[self.i - 1][2]), "width", str(self.nw)]

        return nodedata

    ## not necessary to add node width (nw)
    def edgeData(self, refpath, i, nw, edgedata):
        self.refpath = refpath
        self.i = i
        self.nw = nw
        self.edgedata = edgedata

        edgedata.append((str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2]), str(self.refpath[self.i][1] + self.refpath[self.i][2])))

        return edgedata
