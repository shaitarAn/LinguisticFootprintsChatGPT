#!/bin/bash

DATA="2409gpt4" # 2309gpt3, 2403gpt4, 2407gpt4o, 2409gpt4 (different tasks)

# INPUTDIR is the directory with generated files: main_dir/{corpus}/{persona}/{text files}
INPUTDIR="~/switchdrive/AItextDetect/data_${DATA}/"

# OUTPUTDIR is the main output dir for this data `../$OUTPUTDIR`
OUTPUTDIR="../${DATA}"
mkdir -p $OUTPUTDIR

CONFIG=../../config/config.yaml

python3 generate_bash_config.py $CONFIG

bash run_extract_BiasMT_features.sh $INPUTDIR $OUTPUTDIR

bash run_extract_other_features.sh $INPUTDIR $OUTPUTDIR $CONFIG