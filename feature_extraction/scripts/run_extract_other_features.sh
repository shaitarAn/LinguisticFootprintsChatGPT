#!/bin/bash

INPUTDIR=$1
OUTPUTDIR=$2
CONFIG=$3

# Iterates through all specified corpora to extract features using the TextDescriptives library, including a custom formula for German Flesch Reading Ease.
python3 extract_features.py -i $INPUTDIR -o $OUTPUTDIR

# Restructures data into a more accessible format, sorting by individual features, language, and domain. Iterates through: `$OUTDIR/results/per_corpus/{corpus}`
# - Per Feature: `$OUTDIR/results/per_feature/{feature_to_extract}/{corpus}.csv`
# - Per Language: `$OUTDIR/results/per_language/{language}/{feature}.csv`
# - Per Domain: `$OUTDIR/results/per_domain/news/{language}/{feature}.csv`
python3 combine_results_per_lang_domain.py $OUTPUTDIR $CONFIG

for feature_type in "morphology" "lexical_richness" 

do
    echo $feature_type
    # Pools together and formats results for morphological and lexical features.
#   - Inputs:
#     - Morphological Features: `$OUTDIR/results/morphology/{corpus}.csv`
#     - Lexical Features: `$OUTDIR/results/lexical_richness/{corpus}.csv`
#   - Output Directories:
#     - Per Feature: `$OUTDIR/results/per_feature/{feature_to_extract}/{corpus}.csv`
#     - Per Language: `$OUTDIR/results/per_language/{language}/{feature}.csv`
#     - Per Domain: `$OUTDIR/results/per_domain/news/{language}/{feature}.csv`
    python3 include_BiasMT_features.py -f $feature_type -o "${OUTPUTDIR}/results" -c $CONFIG

done