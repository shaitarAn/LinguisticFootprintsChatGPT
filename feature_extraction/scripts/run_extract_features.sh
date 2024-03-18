#!/bin/bash

for corpus in 'cs_de' 'cs_en' '20min' 'cnn' 'pubmed_de' 'pubmed_en' 'zora_en' 'zora_de' 'e3c' 'ggponc'

do
    echo $corpus
    # python3 extract_features.py --corpus $corpus

done

python3 combine_results_per_lang_domain.py

for feature_type in "morphology" "lexical_richness" 

do
    echo $feature_type
    python3 transform_dataframe.py -f $feature_type

done