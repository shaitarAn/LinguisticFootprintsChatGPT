#!/bin/bash

source corpora_config.sh

DATADIR=$1
out=$2
OUTPUTDIR="${out}/morphology"
mkdir -p $OUTPUTDIR
mkdir -p "${out}/results/morphology"

# Iterate over the corpora
for corpus in $DATADIR/*; do
    corpus_name=$(basename "$corpus")
    
    # Check if the corpus is one of the specified names
    if [[ " ${GERMAN_CORPORA[@]} " =~ " ${corpus_name} " ]]; then
        echo "Processing corpus: $corpus_name"

        outdir=${OUTPUTDIR}/${corpus_name}
        mkdir -p $outdir

        # print the subdirectory names in the corpus
        for persona in $(ls $corpus); do

            echo "Processing personas: $persona"
            
            for file in $corpus/${persona}/*; do
                # echo "Processing file: $file"
                file_name=$(basename "$file" .txt)
                echo "File name: ${file_name}"
                
                python mrph_calculate.py -f ${file} -l "de" -sys "${persona}_$file_name" -dat "${corpus_name}" -o $out -v "${OUTPUTDIR}/freq_voc/${corpus_name}/${persona}_${file_name}.freq_voc" -t 0 > "${outdir}/${persona}_$file_name.txt"
            done
        done
    else
        echo "Skipping corpus: $corpus_name"
    fi
done

