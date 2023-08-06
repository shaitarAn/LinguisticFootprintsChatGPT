

import os
import re
import argparse
from tqdm import tqdm

def file_path(string):
    """Check if string is a valid filepath"""
    if os.path.exists(string):
        return string
    else:
        raise NotADirectoryError


def replace_ref(text:str):
    return re.sub(r"\[\d+(, ?\d+|(.\d+)?)*\]", r"[REF]", text)


def rewrite_file(infilepath, outfilepath):
    with open(infilepath, "r", encoding="utf-8") as infile:
        new_text = replace_ref(infile.read())

    with open(outfilepath, "w", encoding="utf-8") as outfile:
        outfile.write(new_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder", type=file_path)
    parser.add_argument("outfolder", type=str)

    args = parser.parse_args()

    if not os.path.isdir(args.outfolder):
        os.makedirs(args.outfolder)

    for filename in tqdm(os.listdir(args.infolder)):
        infilepath = os.path.join(args.infolder, filename)
        outfilepath = os.path.join(args.outfolder, filename)
        rewrite_file(infilepath, outfilepath)

