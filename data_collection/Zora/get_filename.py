### Script to get the filename from the citation


import hashlib
import os
import re
import json
import argparse

def get_filename(citation, extension):
    citation_hash = hashlib.sha1(citation.encode()).hexdigest()
    year = re.search(r"\((\d{4})\)", citation).group(1)
    return f"{year}-{citation_hash}.{extension}"

def make_dict(infilepath, extension):
    hash_dict = {}
    with open(infilepath, "r", encoding="utf-8") as infile:
        for citation in infile:
            hash_dict[get_filename(citation.strip(), extension)] = citation.strip()

    # sort the dict by year
    return dict(sorted(hash_dict.items()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infilepath", type=str)
    parser.add_argument("--extension", "-e", type=str, default="pdf")
    args = parser.parse_args()

    folder = os.path.split(args.infilepath)[0]
    hash_dict = make_dict(args.infilepath, args.extension)
    with open(os.path.join(folder, "filenames.json"), "w", encoding="utf-8") as outfile:
        json.dump(hash_dict, outfile)

