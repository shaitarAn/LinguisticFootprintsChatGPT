# iterate through a directory and its subdirectories and print the names of the files

import os
import sys
from pathlib import Path
import re
import argparse

# create a parser object
parser = argparse.ArgumentParser()
# add inputdir
parser.add_argument("--inputdir", "-i", type=str, required=True, help="Input directory")
parser.add_argument("--outputdir", "-o", type=str, required=True, help="Output directory")

# parse the arguments
args = parser.parse_args()

inputdir = args.inputdir
outputdir = args.outputdir

for subdir, dirs, files in os.walk(inputdir):
    if subdir == "../output/oov":
        continue
    # print(subdir)
    # calculate the avearge number of tokens in the files in the directory
    tokens_list = []
    for file in files:
        if file == ".DS_Store":
            continue
        # print(file)
        with open(os.path.join(subdir, file), 'r') as f:
            # read the file
            data = f.read()
            # get the number of tokens in the file
            tokens = len(data.split(' '))
            # print(tokens)
            # append the number of tokens to the tokens list
            tokens_list.append(tokens)
    # print(tokens_list)
    average = sum(tokens_list)/len(tokens_list)

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for file in files:
        if file == ".DS_Store":
            continue
        with open(os.path.join(subdir, file), 'r') as f:
            # read the file
            data = f.read()
            # get the number of tokens in the file
            tokens = len(data.split(' '))
            # print(tokens)
            # append the number of tokens to the tokens list
            if tokens > average:
                data = " ".join(data.split(' ')[:int(average)])
            # print(data)
            # write the truncated file to the new directory
            with open(os.path.join(outputdir, file), 'w') as f:
                f.write(data)   