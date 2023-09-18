#!/bin/bash

#  example: ./run_pipeline.sh 1.0 1.0

temp=$1
fp=$2
params=$temp\_$fp

for corpus in 'cnn' 'pubmed_en' 'e3c' 'ggponc'

do

    echo "Running $corpus"
    python3 generate.py -t $temp -fp $fp -c $corpus

    python3 extract_features.py -c $corpus --params $params

    echo "----------------------"

done
