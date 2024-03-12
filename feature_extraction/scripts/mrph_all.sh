#!/bin/bash

# List of German corpora names
GERMAN_CORPORA=("20min")
# pubmed_de" "ggponc" "zora_de" "cs_de

DATADIR="../../data"
lang="de"

# dataset=$(basename "$DATADIR")

cont="continue"

# Iterate over the corpora
for corpus in $DATADIR/*; do
    corpus_name=$(basename "$corpus")
    
    # Check if the corpus is one of the specified names
    if [[ " ${GERMAN_CORPORA[@]} " =~ " ${corpus_name} " ]]; then
        echo "Processing corpus: $corpus_name"
        
        outdir=../results/morphology/${corpus_name}
        mkdir -p $outdir
        
        for system in human ${cont} explain create; do
            echo "Processing system: $system"
            
            for file in $corpus/${system}/*; do
                echo "Processing file: $file"
                file_name=$(basename "$file" .txt)
                echo "File name: ${file_name}"
                
                python mrph_calculate.py -f ${file} -l $lang -sys "${system}_$file_name" -dat "${corpus_name}" -v "freq_voc/${corpus_name}/${system}_${file_name}.freq_voc" -t 0 > "${outdir}/${system}_$file_name.txt"
            done
        done
    else
        echo "Skipping corpus: $corpus_name"
    fi
done

