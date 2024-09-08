#!/bin/bash

# INPUTDIR is the directory with generated files: main_dir/{corpus}/{persona}/{text files}
INPUTDIR=~/switchdrive/AItextDetect/data_2409_gpt4

# OUTPUTDIR is the main output dir for this data `../$OUTPUTDIR`
OUTPUTDIR=../2409
mkdir -p $OUTPUTDIR

# python3 generate_bash_config.py

# bash run_extract_BiasMT_features.sh $INPUTDIR $OUTPUTDIR

bash run_extract_other_features.sh $INPUTDIR $OUTPUTDIR