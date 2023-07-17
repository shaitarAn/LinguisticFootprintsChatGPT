#!/bin/bash

OUTDIR=results_sophistication
mkdir -p $OUTDIR

# DATADIR=$HOME/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/20min

echo "compute the lexical profile (frequency bands: step=1000; last=2000) of datasets"

for system in machine human; do
  echo $system
  python sophistication_calculate.py -f "20min_${system}_all.txt" -sys ${system} -o $OUTDIR/sophistication_20min.csv
#   done
done
