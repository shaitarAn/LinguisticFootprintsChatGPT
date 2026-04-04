DATA="2403gpt4" # 2309gpt3, 2403gpt4, 2407gpt4o, 2409gpt4 (different tasks)

# INPUTDIR is the directory with generated files: main_dir/{corpus}/{persona}/{text files}
INPUTDIR="~/switchdrive/AItextDetect/data_${DATA}/"

CONFIG=../../config/config.yaml

python3 examine_pronouns.py -i $INPUTDIR -c $CONFIG