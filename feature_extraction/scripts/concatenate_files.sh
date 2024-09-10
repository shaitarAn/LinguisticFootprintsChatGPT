#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_directory> <output_directory>"
  exit 1
fi

# Assign arguments to variables
DATADIR=$1
# Ensure input directory ends with a slash
DATADIR="${DATADIR%/}/"

OUTPUT_DIR=$2
# Check if the OUTPUT_DIR directory exists
# create it if it doesn't
if [ ! -d "$OUTPUT_DIR" ]; then
  mkdir -p "$OUTPUT_DIR"
fi
OUTPUT_DIR="${OUTPUT_DIR}/concatenated_data/"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through each corpus folder in the input directory
for corpus_folder in "$DATADIR"*; do
    if [[ -d "$corpus_folder" ]]; then  # Ensure it's a directory
        corpus=$(basename "$corpus_folder")  # Get the corpus name
        echo "**********"
        echo "Processing corpus: $corpus"

        # Loop through each system folder within the corpus folder
        for system_folder in "$corpus_folder"/*; do
            if [[ -d "$system_folder" ]]; then  # Ensure it's a directory
                system=$(basename "$system_folder")  # Get the system name
                echo "Processing system: $system"

                # Initialize or clear the temporary concatenation file
                tmp_file="${OUTPUT_DIR}${corpus}_${system}.tmp"
                : > "$tmp_file"  # Create or truncate the temporary file

                # Loop through files in the system folder
                for file in "$system_folder"/*; do
                    if [[ -f "$file" ]]; then  # Ensure it's a file
                        echo "Appending file: $file"
                        cat "$file" >> "$tmp_file"
                        echo "" >> "$tmp_file"  # Ensure newline after each file
                    fi
                done

                # Remove any extra blank lines and finalize the output file
                final_output="${OUTPUT_DIR}/${corpus}_${system}.txt"
                sed '/^\s*$/d' "$tmp_file" > "$final_output"
                rm "$tmp_file"  # Remove the temporary file
            fi
        done
    fi
done

echo "All corpora processed and files concatenated successfully."
