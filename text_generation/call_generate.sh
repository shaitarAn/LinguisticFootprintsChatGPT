#!/bin/bash

infolder="../data/sample_100_JSON"  # Folder with all the JSON for generation
outfolder="../data/final_files_simple_prompt_2"

prompt_file_de="prompts/simple_prompt_sci_art_de.txt"
prompt_file_en="prompts/simple_prompt_sci_art_en.txt"

#list of inputs
inputs=(
  # "gpt-3.5-turbo $infolder/zora_de.json de --outfolder $outfolder/zora_de --time_log zora_de --prompt_file $prompt_file_de"
  # "gpt-3.5-turbo $infolder/zora_en.json en --outfolder $outfolder/zora_en --time_log zora_en --prompt_file $prompt_file_en"
	# "gpt-3.5-turbo $infolder/20min.json de --outfolder $outfolder/20min --time_log 20min"
	# "gpt-3.5-turbo $infolder/cnn.json en --outfolder $outfolder/cnn --time_log cnn --start_from 60"
	# "gpt-3.5-turbo $infolder/e3c.json en --outfolder $outfolder/e3c --time_log cnn"
	# "gpt-3.5-turbo $infolder/GGPONC.json de --outfolder $outfolder/GGPONC --time_log GGPONC --start_from 87"
	# "gpt-3.5-turbo $infolder/pubmed_de.json de --outfolder $outfolder/pubmed_de --time_log pubmed_de --prompt_file $prompt_file_de"
	# "gpt-3.5-turbo $infolder/pubmed_en.json en --outfolder $outfolder/pubmed_en --time_log pubmed_en --prompt_file $prompt_file_en"
	"gpt-3.5-turbo $infolder/cs_en.json en --outfolder $outfolder/cs_en --time_log cs_en"
	"gpt-3.5-turbo $infolder/cs_de.json de --outfolder $outfolder/cs_de --time_log cs_de"
)
# loop through the inputs and call python file
for input in "${inputs[@]}";
do
	python3 generate.py $input
done