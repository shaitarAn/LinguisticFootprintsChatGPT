#!/bin/bash

DATADIR=$1
OUTPUTDIR=$2

source corpora_config.sh

# Iterate over the corpora
for corpus_folder in $DATADIR/*; do
    corpus=$(basename "$corpus_folder")
    
    # Check if the corpus is one of the specified names
    if [[ " ${GERMAN_CORPORA[@]} " =~ " ${corpus} " ]]; then
        echo "Processing corpus: $corpus"
        
        # Loop through each system folder within the corpus folder
        for system_folder in "$corpus_folder"/*; do
            system=$(basename "$system_folder")
            echo "Processing system: $system"

            for file in ${system_folder}/*; do
                # echo "Processing file: $file"
                python3 most_frequent.py -f ${file} -c ${corpus} -o $OUTPUTDIR
            done
        done
    else
        echo "Skipping corpus: $corpus"
    fi
done
