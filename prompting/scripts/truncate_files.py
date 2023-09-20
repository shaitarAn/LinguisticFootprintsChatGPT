# iterate through a directory and its subdirectories and print the names of the files

import os
import sys
from pathlib import Path

for subdir, dirs, files in os.walk("../output"):
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

    # truncate the files in the directory to the average number of tokens and write them to a new directory
    new_dir = f"../output_truncated/{subdir[10:]}"
    print(new_dir)
    if not os.path.exists(new_dir):
        os.makedirs(new_dir)
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
            with open(os.path.join(new_dir, file), 'w') as f:
                f.write(data)   