#################################
# Create Json files:
#   1. To overview the available text lengths excluding the prompt -> for sampling
#   2. To separate title, prompt and text -> for the Generation with GPT
#################################

import os
from helper import parse_filename, Tokenizer
import json
from tqdm import tqdm
import argparse


def parse_20min(filepath):
    """parse an article from 20 min"""
    with open(filepath, "r", encoding="utf-8") as infile:
        title = infile.readline().strip()
        lead = infile.readline()
        infile.readline()
        first_p = infile.readline()
        prompt = f"{lead}\n{first_p}".strip()
        text = infile.read()

    return title, prompt, text

def parse_cnn(filepath):
    tokenizer = Tokenizer("en")
    with open(filepath, "r", encoding="utf-8") as infile:
        title = infile.readline().strip()
        infile.readline()  # empty line
        text = infile.read()
    prompt, text = tokenizer.split_text(text)
    text = text.strip()
    return title, prompt, text


def parse_pubmed(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        title = infile.readline().strip()[1:]
        infile.readline()
        prompt = infile.readline().strip()
        infile.readline()
        text = infile.read().strip()
    return title, prompt, text


def parse_e3c(filepath):
    tokenizer = Tokenizer("en")
    with open(filepath, "r", encoding="utf-8") as infile:
        text = infile.read()

    prompt, text = tokenizer.split_text(text)
    return "", prompt, text


def parse_GGPONC(filepath):
    tokenizer = Tokenizer("de")
    with open(filepath, "r", encoding="utf-8") as infile:
        title = infile.readline().strip()[1:]
        infile.readline()
        section_title = infile.readline().rstrip()[2:]
        infile.readline()
        text = infile.read()
    prompt, text = tokenizer.split_text(text)
    prompt = section_title +":\n\n" + prompt

    return title, prompt, text


def GGPONC_overview(infolder, outfolder):
    """has a bit of a different structure, thus gets its own funcion..."""
    tokenizer = Tokenizer("de")
    file_dict = {}
    for filename in tqdm(os.listdir(f"{infolder}/GGPONC")):
        filepath = f"{infolder}/GGPONC/{filename}"
        with open(filepath, "r", encoding="utf-8") as infile:
            sickness = infile.readline().strip()[1:]
            infile.readline()
            title = infile.readline()
            infile.readline()
            text = infile.read()
        prompt, text = tokenizer.split_text(text)
        num_tokens, _ = tokenizer.tokenize_text(text)
        file_dict[filename] = {
            "disease": sickness,
            "num_tokens": num_tokens
        }
    with open(f"{outfolder}/GGPONC.json", "w", encoding="utf-8") as outfile:
        json.dump(file_dict, outfile)


def make_json_overview(infolder, outfolder, corpus):
    """Create Overview with the number of tokens after extracting the prompt"""
    parse_function = {
        "20min": parse_20min,
        "cnn": parse_cnn,
        "e3c": parse_e3c,
        "pubmed_de": parse_pubmed,
        "pubmed_en": parse_pubmed

    }
    file_dict = {}
    for filename in tqdm(os.listdir(f"{infolder}/{corpus}")):
        filepath = f"{infolder}/{corpus}/{filename}"
        year, title, num_tokens, lang = parse_filename(filename)
        tokenizer = Tokenizer(lang)
        title, prompt, text = parse_function[corpus](filepath)
        num_tokens, _ = tokenizer.tokenize_text(text)  # number of tokens without the prompt!!
        file_dict[filename] = {
            "year": year,
            "num_tokens": num_tokens
        }

    with open(f"{outfolder}/{corpus}.json", "w", encoding="utf-8") as outfile:
        json.dump(file_dict, outfile)




def make_json_for_generation(infolder:str, outfolder:str, corpus:str,):


    parse_function = {
        "20min": parse_20min,
        "cnn": parse_cnn,
        "e3c": parse_e3c,
        "GGPONC": parse_GGPONC,
        "pubmed_de": parse_pubmed,
        "pubmed_en": parse_pubmed

    }
    wd = f"{infolder}/{corpus}"  # working directory
    filenames = os.listdir(wd)
    text_dict = {}
    for filename in tqdm(filenames):
        filepath = f"{wd}/{filename}"
        title, prompt, text = parse_function[corpus](filepath)
        text_dict[filename] = {
            "title": title,
            "prompt": prompt,
            "text": text
        }

    with open(f"{outfolder}/{corpus}.json", "w", encoding="utf-8") as outfile:
        json.dump(text_dict, outfile)





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("method", type=str, choices=["overview", "generation"], help="Create Json files for what purpose")
    parser.add_argument("infolder", type=str, help="Folder above the Corpus folder")
    parser.add_argument("outfolder", type=str, help="Folder in which to store the JSON files")
    parser.add_argument("corpus", type=str, choices=["20min", "cnn", "e3c", "GGPONC", "pubmed_de", "pubmed_en"])
    args = parser.parse_args()

    if args.method == "overview":
        if args.corpus == "GGPONC":
            GGPONC_overview(args.infolder, args.outfolder)
        else:
            make_json_overview(args.infolder, args.outfolder, args.corpus)
    else:
        make_json_for_generation(args.infolder, args.outfolder, args.corpus)

