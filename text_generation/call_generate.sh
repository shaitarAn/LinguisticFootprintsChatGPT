#!/bin/bash

model="gpt-3.5-turbo-16k"
infolder="../data_collection/100_files_json"  # Folder with all the JSON for generation

outfolder="../data_2403" # in this folder subfolders task/corpus/system will be created

echo $OPENAI_API_KEY

mkdir -p $outfolder

prompt_file="prompts.json"

corpora=("pubmed_de" "pubmed_en" "cnn" "20min" "e3c" "ggponc" "zora_en" "zora_de" "cs_en" "cs_de")  # list of all the corpora to use

time_log="completion_time/data_2403"  #Folder to save the time logs, they are saved as <corpus_name>_date.csv

prompt_types=("explain" "create" "continue")

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
