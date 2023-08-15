
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


def replace_ref(text :str):
    """standardize pubmed citations"""
    # Note I have not dealt with citations with numbers in parentheses
        # -> have not found a way to match them without also matching enumerations
    pattern = r"\[\d+(, ?\d+|(.\d+)?)*\]|" \ 
              r"\(([^\)]|\n)+,? \n?\d{4}(: \d+(\S\d+)?)?\)"  # APA style

    return re.sub(pattern, r"[REF]", text)


def replace_multiple_ref(text :str):
    """replace multiple citations in GGPONC"""
    return re.sub(r"\[REF\](,  ?\[REF\])+", r"[REF]", text)


def rewrite_file(infilepath, outfilepath, rewrite_function):
    with open(infilepath, "r", encoding="utf-8") as infile:
        new_text = rewrite_function(infile.read())

    with open(outfilepath, "w", encoding="utf-8") as outfile:
        outfile.write(new_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, choices=["replace", "replace_multiple"])
    parser.add_argument("infolder", type=file_path)
    parser.add_argument("outfolder", type=str)

    args = parser.parse_args()

    if not os.path.isdir(args.outfolder):
        os.makedirs(args.outfolder)

    if args.mode == "replace":
        rewrite_function = replace_ref
    else:
        rewrite_function = replace_multiple_ref


    for filename in tqdm(os.listdir(args.infolder)):
        infilepath = os.path.join(args.infolder, filename)
        outfilepath = os.path.join(args.outfolder, filename)
        rewrite_file(infilepath, outfilepath, rewrite_function)
