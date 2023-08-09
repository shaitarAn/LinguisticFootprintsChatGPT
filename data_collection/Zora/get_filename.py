### Script to get the filename from the citation


import hashlib
import os
import re
import json
import argparse

def get_filename(citation):
    citation_hash = hashlib.sha1(citation.encode()).hexdigest()
    year = re.search(r"\((\d{4})\)", citation).group(1)
    return f"{year}-{citation_hash}.pdf"

def make_dict(infilepath):
    hash_dict = {}
    with open(infilepath, "r", encoding="utf-8") as infile:
        for citation in infile:
            hash_dict[get_filename(citation.strip())] = citation

    # sort the dict by year
    return dict(sorted(hash_dict.items()))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infilepath", type=str)
    args = parser.parse_args()

    folder = os.path.split(args.infilepath)[0]
    hash_dict = make_dict(args.infilepath)
    with open(os.path.join(folder, "filenames.json"), "w", encoding="utf-8") as outfile:
        json.dump(hash_dict, outfile)

