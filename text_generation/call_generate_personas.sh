#!/bin/bash

## without parameters

model="gpt-4" #gpt-3.5-turbo-16k, gpt-4

outfolder="../data_2403_gpt4" # in this folder subfolders task/corpus/system will be created

infolder="../data_collection/100_files_json/"  # Folder with all the JSON for generation

# echo $OPENAI_API_KEY

mkdir -p $outfolder

prompt_file="prompts.json"

corpora=("pubmed_de" "pubmed_en" "cnn" "20min" "e3c" "ggponc" "zora_en" "zora_de" "cs_en" "cs_de") 

for corpus in "${corpora[@]}";do

    echo "Running $corpus"

    mkdir -p "../output/${corpus}/human/"

    python3 generate_personas.py $model -c $corpus -i $infolder -o $outfolder 

done