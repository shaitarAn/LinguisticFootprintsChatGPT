#!/bin/bash

DATADIR=$1
OUPUTDIR=$2

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_directory> <output_directory>"
  exit 1
fi

source corpora_config.sh
# combine the corpora names GERMAN_CORPORA and ENGLISH_CORPORA
corpus_names=("${GERMAN_CORPORA[@]}" "${ENGLISH_CORPORA[@]}") 

OUTDIR=$OUPUTDIR/results/lexical_richness
mkdir -p $OUTDIR

echo "compute the pairwise lexical diversity standard metrics (TTR, Yules, MTLD) of datasets"

# Loop through all corpus folders
for corpus_folder in $DATADIR/*; do
    corpus=$(basename "$corpus_folder")  # Get the corpus name
    echo "**********"
    echo $corpus

    # if corpus in corpus_names; then
    #     continue
    if [[ " ${corpus_names[@]} " =~ " ${corpus} " ]]; then
        # continue

      # Loop through each system folder within the corpus folder
      for system_folder in "$corpus_folder"/*; do
        system=$(basename "$system_folder")
        echo "system: $system"

        for file in "$system_folder"/*; do
          # continue
          # echo $file

          python lxr_calculate.py -f ${file} -sys ${system} -i 100 -o $OUTDIR/${corpus}.csv

      done
    done

    fi

done

