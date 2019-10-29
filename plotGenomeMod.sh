#!/bin/bash

#For yeast

for file in *.vcf;
do
awk 'BEGIN{OFS="\t"} $1 ~ /^chr*/ {if ($1=="chrII") $2=$2+230218;if ($1=="chrIII") $2=$2+1043402;if ($1=="chrIV") $2=$2+1360022; if ($1=="chrV") $2=$2+2891955; if ($1=="chrVI") $2=$2+3468829; if ($1=="chrVII") $2=$2+3738990;if ($1=="chrVIII") $2=$2+4829930; if ($1=="chrIX") $2=$2+5392573; if ($1=="chrX") $2=$2+5832461; if ($1=="chrXI") $2=$2+6578212; if ($1=="chrXII") $2=$2+7245028; if ($1=="chrXIII") $2=$2+8323205; if ($1=="chrXIV") $2=$2+9247636; if ($1=="chrXV") $2=$2+10031969; if ($1=="chrXVI") $2=$2+11123260; if ($1=="chrM") $2=$2+12071326; $1="GENOME"} {print $0}' $file > genome$file
done
