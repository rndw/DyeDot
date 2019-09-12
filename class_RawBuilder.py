class RawData:

    def __init__(self, key, nw, i, refpath):
        self.key = key
        self.nw = nw
        self.i = i
        self.refpath = refpath

    def nodeData(self, nodedata):
        self.nodedata = nodedata
        # expose key argument for nodes - might need at a later stage

        nodedata[str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2])] = {"label": str(
            self.refpath[self.i - 1][0] + ' ' + self.refpath[self.i - 1][1] + ' ' + self.refpath[self.i - 1][2]), 'ID': self.key,
            "width": str(self.nw)}

        return nodedata

    # not necessary to add node width (nw)
    def edgeData(self, edgedata):
        self.edgedata = edgedata

        edgedata[str(self.refpath[self.i - 1][1] + " " + self.refpath[self.i - 1][2])] ={'To': str(
            self.refpath[self.i][1] + " " + self.refpath[self.i][2]), "label": self.key, 'ID': self.key}

        return edgedata

    def xmlOut(self):
        pass

    def xyCoord(self):
        pass

# TESTING
