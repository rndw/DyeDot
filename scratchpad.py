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
from class_Utils import dataUtils

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

output = VarGraphCons().anchor_builder(dat,path)
RegionOfInterestGraph(output, loci).region()
refpath = RegionOfInterestGraph(output, loci).referencegr()
graph, refnodedata, refedgedata = RefGraphBuilder().referencepath(refpath)

xgraph, varnodedata, varedgedata, allvarnode, allvaredge = RefGraphBuilder().variantpath(output, graph, loci, refpath)

objsToWrite = {'refnodedata':refnodedata, 'refedgedata':refedgedata, 'varnodedata':varnodedata, 'varedgedata':varedgedata, 'allvarnode':allvarnode, 'allvaredge':allvaredge}
graphObjs = {'graph':graph, 'xgraph':xgraph}

dataUtils().resumeBck(objsToWrite=objsToWrite, graphObjs=graphObjs,outDir=outDir)

newobjstowrite = dataUtils().resumeFromBck(bckPath=outDir)

#### Testings

#str(refpath[len(refpath) - 1][1] + refpath[len(refpath) - 1][2])] = ["label", str(refpath[len(refpath) - 1][0] + ' ' + refpath[len(refpath) - 1][1] + ' ' +refpath[len(refpath) - 1][2]), "width", str(nw)]

#edgedata.append(  (str(self.refpath[self.i - 1][1] + self.refpath[self.i - 1][2]),str(self.refpath[self.i][1] + self.refpath[self.i][2]))  )

#i = 1
#nw = 1.2
#edgedata = {}

#edgedata[str(refpath[i - 1][1] + refpath[i - 1][2]),str(refpath[i][1] + refpath[i][2])] = ["label", "nothing"]
# get value via list(edgedata.keys())[index] or list(edgedata.values())[index]

