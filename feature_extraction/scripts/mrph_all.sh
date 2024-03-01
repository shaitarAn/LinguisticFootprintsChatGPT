#!/bin/bash

# Check if at least two arguments were provided
if [ "$#" -lt 2 ]; then
    echo "Usage: $0 corpus_directory language"
    exit 1
fi

# List of German corpora names
GERMAN_CORPORA=("pubmed_de" "ggponc" "zora_de" "cs_de")

DATADIR="$1"
lang="$2"

# dataset=$(basename "$DATADIR")

cont="continue"

# Iterate over the corpora
for corpus in $DATADIR/*; do
    corpus_name=$(basename "$corpus")

    outdir=../results/morphology/${corpus_name}

    mkdir -p $outdir
    
    # Check if the corpus is one of the specified names
    if [[ " ${GERMAN_CORPORA[@]} " =~ " ${corpus_name} " ]]; then
        echo "Processing corpus: $corpus_name"
        
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

# # make a list of german corpora names
# for corpus in $DATADIR/*; do
#   echo $corpus
#   for system in human ${cont} explain create; do
#     echo $system
#     for file in $corpus/${system}/*; do
#       echo $file
#       file_name=$(basename "$file" .txt)
#       echo "${file_name}"
#       python mrph_calculate.py -f ${file} -l $lang -sys "${system}_$file_name" -dat "${dataset}" -v "freq_voc/${dataset}/${system}_${file_name}.freq_voc" -t 0 > "${outdir}/${system}_$file_name.txt"
#     done
#   done
# done




# # iterate through a directory of files
# for system in human ${cont} explain create; do
#   echo "${system}"
#   for file in $DATADIR/${system}/*; do
#     file_name=$(basename "$file" .txt)
#     echo "${file_name}"
#     python mrph_calculate.py -f ${file} -l $lang -sys "${system}_$file_name" -dat "${dataset}" -v "freq_voc/${dataset}/${system}_${file_name}.freq_voc" -t 0 > "${outdir}/${system}_$file_name.txt"
#   done
# done
