#!/bin/bash
# As an argument give a directory with files.
# bash create_most_freq_vocs.sh ~/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/20min/human/*

for i in "$@"
do
  # echo ${i}
  python3 most_frequent.py -f ${i}
done
