#!/bin/bash

OUTDIR=../results/lexical_richness
mkdir -p $OUTDIR

DATADIR="$@"

echo "compute the pairwise lexical diversity standard metrics (TTR, Yules, MTLD) of datasets"

# Loop through all corpus folders
for corpus_folder in $DATADIR*; do
    corpus=$(basename "$corpus_folder")  # Get the corpus name
    echo "**********"
    echo $corpus

    # Loop through each system folder within the corpus folder
    for system_folder in "$corpus_folder"/*; do
      system=$(basename "$system_folder")
      echo $system

      for file in "$system_folder"/*; do

        python lxr_calculate.py -f ${file} -sys ${system} -o $OUTDIR/${corpus}.csv

      done
    done

done

