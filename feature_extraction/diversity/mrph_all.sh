#!/bin/bash

DATADIR=$HOME/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/20min

dataset="20min"

# iterate through a directory of files
for system in human machine; do
  echo "${system}"
  for file in $DATADIR/${system}/*; do
    file_name=$(basename "$file" .txt)
    echo "${file_name}"
    python mrph_calculate.py -f ${file} -l de -sys "${system}_$file_name" -v "freq_voc/${system}_${file_name}.freq_voc" -t 0 > "results_shannon/${dataset}_${system}_$file_name.txt"
  done
done
