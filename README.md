[![Build Status](https://travis-ci.com/rndw/DyeDot.svg?branch=master)](https://travis-ci.com/rndw/DyeDot)
[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
![Code Size](https://img.shields.io/github/languages/code-size/rndw/DyeDot)
![Repo Size](https://img.shields.io/github/repo-size/rndw/DyeDot)  

![Last commit](https://img.shields.io/github/last-commit/rndw/DyeDot)

# Current focus:
[ ] Add XML output for Cytoscape  
[x] Expose data structures to other functions  
[x] Manual plotting - Interactive plotting  
*  [ ] Improve interactive display - Dash

# DyeDot: Variation graphs from VCF

## To run:
Extract the archive containing several yeast vcf files in the VCFs dir. After extracting the archive you should several vcf files in the VCFs directory.

```
.
└── Graph_vars
    ├── class_Grapher.py
    ├── class_parsetools.py
    ├── class_vcf_parser.py
    ├── DRIVER_dyedot.py
    ├── dyedot_example.png
    ├── output.dot
    ├── README.md
    └── VCFs
        ├── DBVPG6044.vcf
        ├── DBVPG6765.vcf
        ├── README.md
        ├── SK1.vcf
        ├── UWOPS03-461.4.vcf
        ├── UWOPS83-787.3.vcf
        ├── UWOPS87-2421.vcf
        ├── vcfs.tar.xz
        ├── Y12.vcf
        ├── Y55.vcf
        └── YPS128.vcf
```

## Install python dependencies:

`pip3 install --upgrade pip`

`pip3 install -r requirements.txt`

## Viewing dot files locally:
**OPTIONAL**
`apt-get install kgraphviewer kgraphviewer-dev`

kgraphviewer displays multiple edges incorrectly. The default is to merge edges, which, defeats the purpose of graphs.

As an alternative, try ZGRViewer. However, the SVG output doesn't colour the node backgrounds and thus limits the number of possible comparisons.

- Currently working on sequenceTubeMap viz.

## Run driver script:
Example command:

`$ python3 DRIVER_dyedot.py -p ./VCFs/ -o output -c chr7 -b 6000 -e 15000`

If you need help:

`python3 DRIVER_dyedot.py -h`

### Quickly view output from included example data
`python3 DRIVER_dyedot.py -p VCF/ -o ./Test/test`  
or  
`python3 DRIVER_dyedot.py`  
or  
`python3 DRIVER_dyedot.py -r True`  

### Repeat run on previous data
DyeDot will use backup and intermediate files from previous runs if available. Just supply the `-r` argument.  

`python3 DRIVER_dyedot.py -r True`

## Notes
Instructions on how to convert a multi-sample vcf file is included in the ./VCFs/readme. A URL with additional vcf files is supplied for download.

DyeDot was only tested on SNP data from yeast as an example. Testing on human data and large structural variants required.

## Interactive visualisation
Convert the graphviz (.dot or .gv) output to .gml format with `dot graph.gv | gv2gml > graph.gml` **OR** `gv2gml graph.dot -o graph.gml` and visualise with `Cytoscape 3.0+` via import.

### View pre-generated output
[plotly interactive figure](DyeDot_LARGESNP_SLIDER.html)   
![plotly static output](dyedot-dotler.png)
