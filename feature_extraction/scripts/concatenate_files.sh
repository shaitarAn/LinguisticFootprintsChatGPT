#!/bin/bash

DATADIR="$@"/*

# Loop through each corpus folder
for corpus_folder in $DATADIR; do
    corpus=$(basename "$corpus_folder")  # Get the corpus name
    ECHO $corpus

    # Loop through each system folder within the corpus folder
    for system_folder in "${corpus_folder}"/human/ "${corpus_folder}"/machine/; do
        system=$(basename "$system_folder")  # Get the system name

        # Concatenate text files within the system folder and save to corpus_system_all.txt
        cat "$system_folder"*.txt > "../data/${corpus}_${system}.txt"
    done
done
