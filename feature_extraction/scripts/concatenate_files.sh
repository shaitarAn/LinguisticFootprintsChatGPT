#!/bin/bash

DATADIR="$@"

# Loop through each corpus folder
for corpus_folder in $DATADIR*; do
    corpus=$(basename "$corpus_folder")  # Get the corpus name
    echo "**********"
    echo $corpus

    # Loop through each system folder within the corpus folder
    for system_folder in "$corpus_folder"/*; do
        system=$(basename "$system_folder")  # Get the system name
        echo $system

        # Loop through files in the system folder
        for file in "$system_folder"/*; do
            echo $file
            
            # Append the file contents to the "../data/${corpus}_${system}.txt" file
            cat "$file" >> "../concatenated_data/${corpus}_${system}.tmp"
            echo " " >> "../concatenated_data/${corpus}_${system}.tmp"

            # awk '1; END {print ""}' "$file" >> "../data/${corpus}_${system}.txt"
        done

        sed -r '/^\s*$/d' ../concatenated_data/${corpus}_${system}.tmp > ../concatenated_data/${corpus}_${system}.txt
        rm ../concatenated_data/${corpus}_${system}.tmp

        
    done
done
