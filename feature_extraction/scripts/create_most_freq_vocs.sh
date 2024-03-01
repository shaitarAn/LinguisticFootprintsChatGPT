#!/bin/bash

# bash create_most_freq_vocs.sh ~/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/{corpus}

DATADIR="$@"
dataset=$(basename "$DATADIR")

GERMAN_CORPORA=("pubmed_de" "ggponc" "zora_de" "cs_de")

cont="continue"

# iterate through directories named huamn, continue, explain, create

# Iterate over the corpora
for corpus in $DATADIR/*; do
    corpus_name=$(basename "$corpus")
    
    # Check if the corpus is one of the specified names
    if [[ " ${GERMAN_CORPORA[@]} " =~ " ${corpus_name} " ]]; then
        echo "Processing corpus: $corpus_name"
        
        for system in human ${cont} explain create; do
            echo "Processing system: $system"

            for file in $corpus/${system}/*; do
                # echo "Processing file: $file"
                python3 most_frequent.py -f ${file} -c ${corpus_name}
            done
        done
    else
        echo "Skipping corpus: $corpus_name"
    fi
done

# for system in human ${cont} explain create; do

#   echo $system
#   for file in $DATADIR/${system}/*; do
#     python3 most_frequent.py -f ${file} -c ${dataset}
#   done
# done
