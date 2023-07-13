# !/usr/bin/env python3
# -*- coding: utf8 -*-



import pandas as pd
import shutil
import json
import os
import argparse

def sample_files(corpus_dict,source_folder , destination_folder, category, num=100, exclude=[]):

    filenames = []
    categories = []
    for filename in corpus_dict:
        if filename not in exclude:
            if corpus_dict[filename]["num_tokens"] > 500:
                filenames.append(filename)
                categories.append(corpus_dict[filename][category])
    files_df = pd.DataFrame({"category":categories, "filename": filenames})
    try:
        sample = files_df.sample(num)
    except ValueError:
        print("Population too small: ", len(files_df["category"]))
        overlap = num - len(files_df.index)
        exclude_files_df = pd.DataFrame({"category": [corpus_dict[f][category] for f in corpus_dict if f in exclude],
                                 "filename": [f for f in corpus_dict if f in exclude]})

        overlapped_sample = exclude_files_df.sample(overlap)
        sample = pd.concat([files_df, overlapped_sample])

    print("Distribution of the sample over the categories:")
    print(sample.groupby(["category"]).count())

    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for filename in sample["filename"]:
        shutil.copyfile(f"{source_folder}/{filename}", f"{destination_folder}/{filename}")

def from_raw_to_100(corpus:str):
    with open(f"{corpus}.json", "r", encoding="utf-8") as infile:
        corpus_dict = json.load(infile)

    if corpus == "GGPONC":
        category = "disease"
    else:
        category = "year"

    sample_files(corpus_dict, f"raw/{corpus}", f"100_files/{corpus}", category=category)




    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("corpus", type=str, choices=["20min", "cnn", "e3c", "GGPONC", "pubmed_en", "pubmed_de"])
    parser.add_argument("source_folder", type=str, help="directory above the corpus")
    parser.add_argument("dest_folder", type=str)
    parser.add_argument("--number", "-n", type=int, help="number of files to be sampled")
    parser.add_argument("--exclude", "-e", type=str, help="path to folder with files that are to be excluded" )

    args = parser.parse_args()
    print(args.exclude)

    if args.exclude:
        exclude = os.listdir(args.exclude)
    else:
        exclude = []

    with open(f"overview/{args.corpus}.json", "r", encoding="utf-8") as infile:
        corpus_dict = json.load(infile)

    if args.corpus == "GGPONC":
        category = "disease"
    else:
        category = "year"

    sample_files(corpus_dict, f"{args.source_folder}/{args.corpus}", f"{args.dest_folder}/{args.corpus}",
                 category, num=args.number, exclude=exclude)

    # from_raw_to_100("e3c")


