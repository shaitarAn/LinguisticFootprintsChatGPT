#!/bin/bash

# bash create_most_freq_vocs.sh ~/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/{corpus}

DATADIR="$@"
dataset=$(basename "$DATADIR")

for system in human machine; do
  echo $system
  for file in $DATADIR/${system}/*; do
    python3 most_frequent.py -f ${file} -c ${dataset}
  done
done
