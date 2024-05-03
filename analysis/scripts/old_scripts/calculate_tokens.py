# iteate through a directory of files and calculate the number of tokens in each file and the total number of tokens in the directory

import os
import sys
import json
from pathlib import Path
import pandas as pd


input_dir = os.path.expanduser("~/switchdrive/IMAGINE_files/chatGPT/project_2_gpt_personas/100_files_json/")

print(input_dir)

# create a list to store the number of tokens in each file
tokens_list = []

# uterate through the files in the input directory
for filename in os.listdir(input_dir):
    # open the file
    try:
        with open(os.path.join(input_dir, filename), 'r') as f:
            # read the file
            data = json.load(f)
            for file in data:
                print(file)
                print(data[file]["title"])
                print(data[file]["prompt"])
                # print(data[file]["text"])
                print("--------------------------------------------------")
                # get the number of tokens in the file
                # tokens = len(data[file]["title"].split(' ')) + len(data[file]["prompt"].split(' '))
                tokens  = len(data[file]["text"].split(' '))
                # append the number of tokens to the tokens list
                tokens_list.append(tokens)
    except UnicodeDecodeError:
        print("UnicodeDecodeError")
        # print(filename)
            
# print(tokens_list)
# print(len(tokens_list))
print(sum(tokens_list)/8)
