#!/bin/bash

# assign a string value to a variable
feauture=$"connectives_total"

# print the value of the variable on screen
echo $feauture

for corpus in 'cnn' '20min' 'pubmed_en' 'pubmed_de' 'zora_en' 'zora_de' 'e3c' 'GGPONC'

do

    echo $corpus
    echo "********"
    echo "gpt"

    awk -F',' 'NR > 1 {sum += $1; count++} END {if (count > 0) print sum / count}' ../../feature_extraction/output/paired_features_${corpus}/${feauture}.csv

    echo "human"
    awk -F',' 'NR > 1 {sum += $2; count++} END {if (count > 0) print sum / count}' ../../feature_extraction/output/paired_features_${corpus}/${feauture}.csv

    echo "-------------------"

done