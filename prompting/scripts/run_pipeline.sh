#!/bin/bash

#  example: ./run_pipeline.sh cnn 1.0 1.0

# 'cnn' '20min' 'pubmed_en' 'pubmed_de' 'zora_en' 'zora_de' 'e3c' 'ggponc'

# assign a string value to a variable
corpus=$1
temp=$2
fp=$3
params=$temp\_$fp

echo params: $params

python3 generate.py -t $temp -fp $fp -c $corpus

python3 extract_features.py -c $corpus --params $params
