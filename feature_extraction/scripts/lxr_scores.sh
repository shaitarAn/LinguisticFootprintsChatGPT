#!/bin/bash

OUTDIR=../results/lexical_richness
mkdir -p $OUTDIR

DATADIR="$@"
dataset=$(basename "$DATADIR")

echo "compute the pairwise lexical diversity standard metrics (TTR, Yules, MTLD) of datasets"

for system in machine human; do
  echo $system
  for file in $DATADIR/${system}/*; do
  # append results to file
  python lxr_calculate.py -f ${file} -o $OUTDIR/${dataset}_$system.csv
  done
done

