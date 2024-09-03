#!/bin/bash

DATA_DIR=$1

OUTDIR=../$DATA_DIR/results/sophistication
mkdir -p $OUTDIR

echo $DATA_DIR

# Loop through each text file in the data directory
for file in "../$DATA_DIR"/concatenated_data/*.txt; do
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
    python sophistication_calculate.py -f "$file" -sys "$system" -c "$corpus" -o "$OUTDIR/sophistication_scores.csv"
done
