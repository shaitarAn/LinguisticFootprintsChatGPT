#!/bin/bash

OUTDIR=results_lexical_richness
mkdir -p $OUTDIR

DATADIR=$HOME/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/20min

echo "compute the pairwise lexical diversity standard metrics (TTR, Yules, MTLD) of datasets"

for system in machine human; do
  echo $system
  for file in $DATADIR/${system}/*; do
  # append results to file
  python lxr_calculate.py -l de -f ${file} -o $OUTDIR/lxr_$system.csv
  done
done

