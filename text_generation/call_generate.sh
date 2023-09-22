#!/bin/bash

model="gpt-3.5-turbo-16k"
infolder="../data/sample_5_JSON"  # Folder with all the JSON for generation

outfolder="../data/test_new_script" # in this folder subfolders task/corpus/system will be created

prompt_file="../prompting/scripts/prompts.json"

corpora=("pubmed_de" "pubmed_en")  # list of all the corpora to use

time_log="completion_time/test_new_script"  #Folder to save the time logs, they are saved as <corpus_name>_date.csv

prompt_types=("continue" "explain" "create")

# this can be expanded, but then would have to save it in a different folder for each parameter version
temps=("1")
freq_pens=("1")

for temp in "${temps[@]}";do
  for freq_pen in "${freq_pens[@]}";do
    for prompt_type in "${prompt_types[@]}";do
      for corpus in "${corpora[@]}";do
        echo "Generation in progress. prompt type: $prompt_type, Corpus: $corpus, temp:$temp, freq_pen:$freq_pen"
        python3 generate.py $model $infolder/$corpus.json $corpus --outfolder $outfolder/$prompt_type \
        --prompt_file $prompt_file --prompt_type $prompt_type \
        --time_log $time_log \
        --temp $temp --freq_pen $freq_pen
      done
    done
  done
done
