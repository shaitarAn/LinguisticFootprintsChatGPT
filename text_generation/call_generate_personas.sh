#!/bin/bash

model="gpt-4" #"gpt-4-turbo-2024-04-09" #gpt-3.5-turbo-16k, gpt-4o

outfolder="../data_2409_gpt4" # in this folder subfolders task/corpus/system will be created

# make sure the folder exists
mkdir -p $outfolder

infolder="../data_collection/100_files_json/"  # Folder with all the JSON for generation

# echo $OPENAI_API_KEY

prompt_file="prompts_ashuman_asmachine.json" # "prompts.json"

config_file="../config/config.yaml"

python3 generate_personas.py $model -i $infolder -o $outfolder -p $prompt_file -c $config_file