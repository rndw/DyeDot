from random import randint
from graphviz import Digraph
import seaborn as sns
from class_RawBuilder import rawData

class RefGraphBuilder():

    def __init__(self):
        pass

    def referencepath(self,refpath):
        self.refpath = refpath
        key = 'REFERENCE'
        ## colour setup
        graphcol = 'black'
        graphcolfill = 'grey'
        graphcoledge = 'black'
        ##
        p = Digraph(name=key, node_attr={'shape': 'cds', 'color': graphcol, 'fillcolor': graphcolfill, 'fixedsize':'true'}, format='png',graph_attr={'splines': 'spline', 'rankdir': 'LR'},engine='dot',edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': graphcoledge,'penwidth':'2'})
        nw = 0
        nodedata = {}
        edgedata = {}
        for i in range(1, len(self.refpath) - 1):  # Has to start at one, else loopback in graph
            nw = (int(refpath[i+1][1]) - int(refpath[i][1])) / 10
            if nw < 1.2:
                nw = 1.2
            ##### Return a dictionary of node attr to work with - interactive plotting
            #nodedata[str(self.refpath[i - 1][1] + self.refpath[i - 1][2])] = ["label", str(self.refpath[i - 1][0] + ' ' + self.refpath[i - 1][1] + ' ' + self.refpath[i - 1][2]), "width", str(nw)]
            nodedata = rawData().nodeData(refpath=self.refpath, i=i, nw=nw, nodedata=nodedata, key=key)
            #####
            p.node(self.refpath[i - 1][1] + self.refpath[i - 1][2],label=str(self.refpath[i - 1][0] + ' ' + self.refpath[i - 1][1] + ' ' + self.refpath[i - 1][2]), width = str(nw))
            #### NEED TO ADD FOR EDGES AS WELL
            p.edge(self.refpath[i - 1][1] + self.refpath[i - 1][2], self.refpath[i][1] + self.refpath[i][2])
            edgedata = rawData().edgeData(refpath=self.refpath, i=i, nw=nw, edgedata=edgedata, key=key)

        ## add second last and last node - edge case
        p.node(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],label=str(self.refpath[len(self.refpath) - 2][0] + ' ' + self.refpath[len(self.refpath) - 2][1] + ' ' + self.refpath[len(self.refpath) - 2][2]))
        p.node(self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2],label=str(self.refpath[len(self.refpath) - 1][0] + ' ' + self.refpath[len(self.refpath) - 1][1] + ' ' + self.refpath[len(self.refpath) - 1][2]))
        ## special edgecase nodes (pun intended)
        nodedata[str(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2])] = ["label", str(self.refpath[len(self.refpath) - 2][0] + ' ' + self.refpath[len(self.refpath) - 2][1] + ' ' + self.refpath[len(self.refpath) - 2][2]), "width", str(1.2)]
        nodedata[str(self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2])] = ["label", str(self.refpath[len(self.refpath) - 1][0] + ' ' + self.refpath[len(self.refpath) - 1][1] + ' ' + self.refpath[len(self.refpath) - 1][2]), "width", str(1.2)]

        ##
        p.edge(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2],self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2])
        edgedata[str(self.refpath[len(self.refpath) - 2][1] + self.refpath[len(self.refpath) - 2][2]), str(self.refpath[len(self.refpath) - 1][1] + self.refpath[len(self.refpath) - 1][2])] = ["label" , "Ref"]
        #edgedata[str(refpath[i - 1][1] + refpath[i - 1][2]), str(refpath[i][1] + refpath[i][2])] = ["label", "nothing"]
        ## Not adding descriptor nodes/edges yet
        p.node(str('REF'), label=str('Reference'),  width = '1.6')
        p.node(str('REF_'), label=str('Path'))
        p.edge('REF', 'REF_')

        #print(nodedata)
        return p, nodedata, edgedata;

    def variantpath(self, output,graph,loci,refpath):

        self.output = output
        self.graph = graph
        self.loci =loci
        self.refpath = refpath

        colour = sns.color_palette("colorblind", desat=.5) + sns.color_palette("Set1", n_colors=8, desat=.5)
        del colour[7:9]
        colour = sns.color_palette(colour)
        colour = colour.as_hex()
        graphcol = colour[randint(0, len(colour) - 1)]
        graphcolfill = colour[randint(0, len(colour) - 1)]

        graphcoledge = colour[randint(0, len(colour) - 1)]


        ## newvar
        allvar = {}
        allvaredge = {}
        allvarnode = {}
        testref = [list(elem) for elem in refpath]
        ## newvar

        for key in self.output:
            varpath = ()
            for i in self.output[key]:
                if i[0] == self.loci[0] and int(i[1]) >= self.loci[1] and int(i[1]) <= self.loci[2]:
                    varpath = sorted(
                        tuple(varpath) + (([i[0], i[1], i[3]]),))  # have to convert to int for sort - see refpath
                    varpath = sorted(varpath, key=lambda x: int(x[1]))
            ## newvar
            nw = 0
            temp = []
            matching = []
            ## newvar


            ### expose graph variables to other functions

            x = Digraph(name=key, node_attr={'shape': 'cds', 'color': graphcol,'fillcolor': graphcolfill} , engine='dot',edge_attr={'arrowhead': 'vee', 'arrowsize': '0.5', 'color': graphcoledge,'penwidth':'4'})  # colour can also be set to use x11 names 'red'
            varnodedata = {}
            varedgedata = {}
            for i in range(1, len(varpath) - 1):
                # if output[key][i][0] == loci[0] and int(output[key][i][1]) >= loci[1] and int(output[key][i][1]) <= loci[2]:

                nw = (int(varpath[i+1][1]) - int(varpath[i][1])) / 10
                if nw < 1.2: # have to include a maximum node size as well
                    nw = 1.2
                if varpath[i - 1] in testref:

                    x.node(varpath[i - 1][1] + varpath[i - 1][2],label=str(varpath[i - 1][0] + ' ' + varpath[i - 1][1] + ' ' + varpath[i - 1][2]), width=str(nw))
                    ## Add variant node manual plotting
                    varnodedata = rawData().nodeData(refpath=varpath, i=i, nw=nw, nodedata=varnodedata, key=key)
                    #####

                    matching = list(filter(lambda k: varpath[i] in allvar[k], allvar.keys()))
                    if matching: # exit pathways to a reference node
                        matching.append(key)
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(' - '.join(matching)), color='black', style='dotted')
                        ################
                        ################ rethink how you're storing edges - rather use a dict of tuples to which you add additional data
                        varedgedata = rawData().edgeData(refpath=varpath, i=i, nw=nw, edgedata=varedgedata, key=key)
                        matching = []
                    else:
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(key))
                        varedgedata = rawData().edgeData(refpath=varpath, i=i, nw=nw, edgedata=varedgedata, key=key)

                else:
                    x.node(varpath[i - 1][1] + varpath[i - 1][2],label=str(varpath[i - 1][0] + ' ' + varpath[i - 1][1] + ' ' + varpath[i - 1][2]),width=str(nw))
                    varnodedata = rawData().nodeData(refpath=varpath, i=i, nw=nw, nodedata=varnodedata, key=key)
                    matching = list(filter(lambda k: varpath[i] in allvar[k], allvar.keys()))
                    if matching:  ####################
                        matching.append(key)

                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2],label=str(' - '.join(matching)), color='black', style='dotted')
                        matching = []
                    else:
                        x.edge(varpath[i - 1][1] + varpath[i - 1][2], varpath[i][1] + varpath[i][2], label=str(key))

            ## edge case nodes
            x.node(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2], label=str(varpath[len(varpath) - 2][0] + ' ' + varpath[len(varpath) - 2][1] + ' ' + varpath[len(varpath) - 2][2]))

            x.node(varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2], label=str(varpath[len(varpath) - 1][0] + ' ' + varpath[len(varpath) - 1][1] + ' ' + varpath[len(varpath) - 1][2]))
            varnodedata[str(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2])] = ["label", str(varpath[len(varpath) - 2][0] + ' ' + varpath[len(varpath) - 2][1] + ' ' + varpath[len(varpath) - 2][2]), "width", str(1.2)]
            varnodedata[str(varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2])] = ["label", str(varpath[len(varpath) - 1][0] + ' ' + varpath[len(varpath) - 1][1] + ' ' + varpath[len(varpath) - 1][2]), "width", str(1.2)]


            x.edge(varpath[len(varpath) - 2][1] + varpath[len(varpath) - 2][2],varpath[len(varpath) - 1][1] + varpath[len(varpath) - 1][2])



            ## Not adding descriptor nodes/edges yet
            x.node(str(key), label=str(key))
            x.node(str(key + '_'), label=str('Path'))
            x.edge(str(key), str(key + '_'))

            temp = [_ for _ in varpath if _[2] != 'REF']
            allvar[key] = temp

            self.graph.subgraph(x)
            allvarnode.update(varnodedata)
            allvaredge.update(varedgedata)
        return graph, varnodedata, varedgedata, allvarnode, allvaredge;

