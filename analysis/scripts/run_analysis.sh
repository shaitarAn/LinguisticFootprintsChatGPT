#!/bin/bash

# alphas: 0.01, 0.05
# methods: bon (bonferroni), bh (benjamini-hochberg)
alpha=$1
method=$2

for language in "english" "german"; do
    python3 run_stats_tests.py $language -a $alpha -m $method
done

python3 combine_lang_sign_feats.py -a $alpha -m $method

python3 create_new_heatmap.py
# prints a latex table for the paper into the terminal