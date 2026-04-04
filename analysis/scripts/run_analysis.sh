#!/bin/bash

# alphas: 0.01, 0.05
# methods: bon (bonferroni), bh (benjamini-hochberg)
alpha=$1
method=$2

# make sure yaml file is up to date
config=../../config/config.yaml

generation="2309gpt3"

input_dir="../../feature_extraction/${generation}/results"

for language in "english"; do
    python3 run_stats_tests.py $language -a $alpha -m $method -c $config -i $input_dir
done

python3 combine_lang_sign_feats.py -a $alpha -m $method -c $config -i $input_dir

# python3 create_new_heatmap.py
# prints a latex table for the paper into the terminal
# python3 make_tab4_all_feats_heatmap.py -a $alpha -m $method