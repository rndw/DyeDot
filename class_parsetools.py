class Ptools():

    def __init__(self):
        pass

    def head(self, n=10):
        return self[:n]

    def tail(self, n=10):
        return self[len(self) - n - 1:]

class dataUtils():

    def __init__(self):
        pass

    def resumeBck(self,graph, refnodedata, refedgedata, xgraph, varnodedata, varedgedata, allvarnode, allvaredge):
