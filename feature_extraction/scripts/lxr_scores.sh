#!/bin/bash

OUTDIR=../results/lexical_richness
mkdir -p $OUTDIR

DATADIR="$@"
dataset=$(basename "$DATADIR")
contin="continue"

echo "compute the pairwise lexical diversity standard metrics (TTR, Yules, MTLD) of datasets"

for system in human ${contin} explain create; do
  echo $system
  for file in $DATADIR/${system}/*; do
  # append results to file
  mkdir -p $OUTDIR/${dataset}
  python lxr_calculate.py -f ${file} -o $OUTDIR/${dataset}/$system.csv
  done
done

