#!/bin/bash

# DATADIR=$HOME/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/20min

OUTDIR=../results/sophistication
mkdir -p $OUTDIR

# Loop through each text file in the data directory
for file in ../data/*.txt; do
    # Extract corpus name from the file name
    # Extract everything before the last underscore as "corpus"
    filename=$(basename "$file") 
    corpus="${filename%_*}"

    # Extract the last word before the period as "system"
    system="${filename%.*}"
    system="${system##*_}"

    # Print the results
    echo "Corpus: $corpus"
    echo "System: $system"

    # Run your Python script on the current file and save the results
    python sophistication_calculate.py -f "$file" -sys "$system" -o "$OUTDIR/${corpus}.csv"
done
