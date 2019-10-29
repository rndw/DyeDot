#!/usr/bin/python3

from os import name
import os
from time import time
#import statistics as stats
import math
import argparse
from class_vcf_parser import ReadVcfs, VarGraphCons, RegionOfInterestGraph
from class_Grapher import RefGraphBuilder
from class_Utils import DataUtils
from class_PlotIG import PrepPlotData, PPlot



## GUI
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QPushButton, QVBoxLayout, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon

## Build application class
from PyQt5.QtWidgets import (QMainWindow, QTextEdit,QAction, QFileDialog, QApplication)
from PyQt5.QtGui import QIcon
import sys


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.statusBar()

        openFile = QAction(QIcon('open.png'), 'Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip('Open new File')
        openFile.triggered.connect(self.showDialog)

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(openFile)

        self.setGeometry(300, 300, 350, 300)
        self.setWindowTitle('File dialog')
        self.show()

    def showDialog(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', '/home')

        if fname[0]:
            f = open(fname[0], 'r')

            with f:
                data = f.read()
                self.textEdit.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

## Old work


app = QApplication([])

#label = QLabel('Dotler/DyeDot')
#label.show()

window = QWidget()
layout = QVBoxLayout()
QtGui.QFileDialog.getExistingDirectory(self, 'Select directory')
layout.addWidget(QPushButton('Top'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)

window.show()
app.exec_()


#PARSER FOR CMD ARGUMENTS
parser = argparse.ArgumentParser(description='Read in vcf files and constructs a variations graph', prog='DyeDot')
parser.add_argument('-p', metavar='<path>', nargs='?', default= os.getcwd() + '/VCF', type=str, help="Path to vcf files")
parser.add_argument('-o', type=str, metavar='<filename>', nargs='?', default='DyeDotOutput/DDoutputfile', const='DyeDotOutput/DDoutputfile', help="Output filename (default: ./DyeDotOutput/DDoutputfile)")
parser.add_argument('-c', type=str, metavar='chromosome', nargs='?', default='DEFAULT', const='DEFAULT', help='Chromosome to investigate (default: First element in graph dictionary)')
parser.add_argument('-b', type=int, metavar='integer', nargs='?', default=0, const=0, help='Start location of region to investigate (default: 0 bp)')
parser.add_argument('-e', type=int, metavar='integer', nargs='?', default=20000, const=20000, help='End location of region to investigate (default: 20 000 bp)')
parser.add_argument('-r', type=str, metavar='bool', nargs='?', default=False, const='False', help='Should Dyedot resume from a backup. If set, -R required. (default: False)')
#parser.add_argument('-R', type=str, metavar='<path>', nargs='?', default='./DyeDotOutput', const='./DyeDotOutput', help='Path to Dyedot resume directory (default: ./)')
args = parser.parse_args()

#FRIENDLY CMD ARGUMENT CORRECTION/WARNING/NOTIFICATIONS

outDir = os.getcwd() + "/DyeDotOutput"
try:
    os.mkdir(outDir)
except FileExistsError:
    print("Directory exists, files will be overwritten!")
    pass
finally:
    print(f"Output directory: {outDir}")

print(f"Output will be written to {args.o}.dot: ")
print(f"The region of interest is: {args.c}:{args.b}-{args.e}")
path = args.p
#CHECK OS AND CORRECT PATH IF REQUIRED
## write this into a class (Utils)
if name == 'posix' and path.endswith('/'):
    print(f'Path is: {args.p}')
if name != 'posix' and path.endswith('\\'):
    print(f'Path is: {args.p}')
if name == 'posix' and not path.endswith('/'):
    path = path + '/'
    print(f'Path set to: {path}')
if name != 'posix' and not path.endswith('\\'):
    path = path + '\\'
    print(f'Path set to: {path}')
#CONSTRUCT RANGE OBJECT
# Are we resuming or not
if not args.r:
    #Default: loci = ['chrI',0,50000]
    loci = [args.c, args.b, args.e]

    #path = '/home/rndw/Github/RefGraph/Dyedot_variationGraphs/Small_vcfs/'

    #CREATE A DICTIONARY OBJECT LINKING EACH KEY TO A VCF
    dat = ReadVcfs(path).variant_builder()
    #EXIT IF THE DIR CONTAINS NO VCFs
    if not dat:
        print(f"No vcf files in directory. Please check path: {path}")
        exit(1)

    #UTILITY - WALL TIME. IF SSD OR FAST RAID SETUP, THREADING IMPROVES SPEED BY A FEW SECONDS. SLOWS DOWN WHEN ON MECHANICAL DSK
    start = time()
    #READ IN VCF FILES AS A DICT - EACH VARIANT IS A TUPLE(CHR, POS, ALT, REF) PER VCF/KEY
    ## -- Saving intermediate files in same dir as vcfs
    #Manual run : output = VarGraphCons().anchor_builder(dat)
    output = VarGraphCons().anchor_builder(dat, path)
    #LIMIT DATA TO SPECIFIED REGION
    #IMPROVEMENT: OUTPUT MULTIPLE RANGES OR BLOCKS
    RegionOfInterestGraph(output, loci).region()
    #CONSTRUCT A REFERENCE PATH OBJECT. THIS COULD BE ANYTHING REALLY (HAPLOTYPES) - AS LONG AS IT CONTAINS OVERLAPPING NODES
    refpath = RegionOfInterestGraph(output, loci).referencegr()

    #CONSTRUCT THE REFERENCE PATH
    graph, refnodedata, refedgedata = RefGraphBuilder(refpath=refpath).referencepath()

    #CONSTRUCT THE VARAINT PATHS: BUILT ON TOP OF THE REFERENCE PATH
    xgraph, varnodedata, varedgedata, allvarnode, allvaredge = RefGraphBuilder(refpath=refpath).variantpath(output, graph, loci, refpath)

    #Write objects to disk to resume
    #This would work better as a dictionary - why did I make it a list? - DONE
    objsToWrite = {'refnodedata':refnodedata, 'refedgedata':refedgedata, 'varnodedata':varnodedata, 'varedgedata':varedgedata, 'allvarnode':allvarnode, 'allvaredge':allvaredge}
    graphObjs = {'graph':graph, 'xgraph':xgraph}
    DataUtils().resumeBck(objsToWrite=objsToWrite, graphObjs=graphObjs,outDir=outDir)

## Work on adding to main workflow - Done
if args.r:
    # timing
    start = time()

    outDir = os.getcwd() + "/DyeDotOutput"
    objsToWrite, graphObjs = DataUtils().resumeFromBck(bckPath=outDir)
    #Again, if this was a dict, we wouldn't have to hardcode idx - DONE
    graph = graphObjs['graph']
    xgraph = graphObjs['xgraph']
    refnodedata = objsToWrite['refnodedata']
    refedgedata = objsToWrite['refedgedata']
    varnodedata = objsToWrite['varnodedata']
    varedgedata = objsToWrite['varedgedata']
    allvarnode = objsToWrite['allvarnode']
    allvaredge = objsToWrite['allvaredge']

#ANOTHER FRIENDLY MESSAGE - OUTPUT FILE
print(f'Writing output to: {str(args.o+".dot")}')
#SAVE THE GRAPH IN DOT FORMAT
#IMPROVEMENT: LOOK AT ALTERNATIVE ALGORITHMS/ENGINES - MAYBE NEATO?
graph.save(filename=str(args.o+'.dot'))

# MANUAL PLOTTING
# COORDINATES
from class_PlotIG import PrepPlotData, PPlot
scaleYmin = (len(allvarnode.keys())/2) - 2
scaleYmax = (len(allvarnode.keys())/2) + 2
node_xc, node_yc, edge_xc, edge_yc, VARyl, REFy = PrepPlotData(refedgedata, refnodedata, allvarnode, allvaredge).RefPrepIGData()

import plotly.graph_objs as go

layout = go.Layout(yaxis=dict(range=[scaleYmin, scaleYmax]), xaxis=dict(range=[0, 500]))
fig = go.Figure(layout=layout)

fig = PPlot(node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig).RefBase()

## Vargraphs
##testing
# keys are ['mf1small', 'j11small', 'yi38small']
#key = 'yi38small'
#VARy = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).yScaler(VARyl)
#node_xc, node_yc, edge_xc, edge_yc = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).VarPrepIGData(key, VARy)
#VARyl.remove(VARyl[0])
#xlabs = [allvarnode[key][_]['label'] for _ in allvarnode[key].keys()]
#fig = PPlot(node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig).VarG(xlabs, key)
#fig.layout.update(title=go.layout.Title(text='Chromosome', xref='paper', x=0), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Coordinates')))
#fig.write_html(str(outDir + '/' + 'DyeDot_int_output.html'))
##testing



for key in list(allvarnode.keys()):
    VARy = PrepPlotData(refedgedata, refnodedata, allvarnode, allvaredge).yScaler(VARyl)
    node_xc, node_yc, edge_xc, edge_yc = PrepPlotData(refedgedata, refnodedata, allvarnode,allvaredge).VarPrepIGData(key, VARy)
    VARyl.remove(VARyl[0])
    xlabs = [allvarnode[key][_]['label'] for _ in allvarnode[key].keys()]
    fig = PPlot(node_xc, node_yc, edge_xc, edge_yc, allvarnode, refnodedata, fig).VarG(xlabs, key)



fig.layout.update(title=go.layout.Title(text='Chromosome', xref='paper', x=0), xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text='Coordinates')), xaxis_rangeslider_visible=True)

## testing y scaling

##

fig.write_html(str(outDir + '/' + 'DyeDot_int_output.html'))

#PRINT TIME TAKEN ~ 80s FOR TEST DATA
end = time()
print(end - start)

