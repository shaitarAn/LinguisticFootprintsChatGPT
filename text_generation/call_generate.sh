#!/bin/bash

#list of inputs
inputs=(
	"gpt-3.5-turbo 100_files/JSON/20min.json de --outfolder prompt_test1/20min --start_from 96 --prompt_file prompts/20min/test1.txt"
	# "gpt-3.5-turbo 100_files/JSON/cnn.json en --outfolder prompt_test1/cnn --start_from 95 --prompt_file prompts/cnn/test1.txt"
	# "gpt-3.5-turbo 100_files/JSON/e3c.json en --outfolder prompt_test1/e3c --start_from 95 --prompt_file prompts/e3c/test1.txt"
	# "gpt-3.5-turbo 100_files/JSON/GGPONC.json de --outfolder prompt_test1/GGPONC --start_from 95 --prompt_file prompts/GGPONC/test1.txt"
	# "gpt-3.5-turbo 100_files/JSON/pubmed_de.json de --outfolder prompt_test1/pubmed_de --start_from 91 --prompt_file prompts/pubmed_de/test1.txt"
	# "gpt-3.5-turbo 100_files/JSON/pubmed_en.json en --outfolder prompt_test1/pubmed_en --start_from 95 --prompt_file prompts/pubmed_en/test1.txt"
)
# loop through the inputs and call python file
for input in "${inputs[@]}";
do
	python3 generate.py $input
done