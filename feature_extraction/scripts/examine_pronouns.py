# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import spacy
import os
import re
import argparse
import spacy_udpipe
from collections import defaultdict
import yaml

'''
writes results to ../results/per_corpus
'''

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# ########################################################################
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_dir', required=True, help="Directory with generated data.")
parser.add_argument('-c', '--config', required=True, help="Path to the configuration file.")

args = parser.parse_args()

config = load_config(args.config)
tasks = config['tasks']

GERMAN_CORPORA = config['corpora']['german']
ENGLISH_CORPORA = config['corpora']['english']
# ########################################################################

spacy_udpipe.download("en")
spacy_udpipe.download("de")

nlp = spacy.load('en_core_web_lg')
Dnlp = spacy.load('de_core_news_lg')

def find_pronouns(lang, file_path, average):
    if lang == 'en':
        nlp = spacy.load('en_core_web_lg')
    else:
        nlp = spacy.load('de_core_news_lg')

    with open(file_path, 'r') as f:
        text = f.read()
        if len(text.split()) > average:
            text = " ".join(text.split()[:int(average)])

        if lang == 'de':
            doc = Dnlp(text)
        else:
            doc = nlp(text)
        pronouns = defaultdict(int)
        for token in doc:
            if token.pos_ == 'PRON':
                pronouns[token.text] += 1

    return pronouns

def main(corpus, results):
    corpus_name = corpus.split("/")[-1]
    if corpus_name in ENGLISH_CORPORA:
        lang = 'en'
    else:
        lang = 'de'

    input_dir = os.path.expanduser(os.path.join(args.input_dir, corpus))
    num_files = len(os.listdir(f"{input_dir}/human/"))

    # Dictionary to hold combined pronoun counts for this corpus
    combined_counts = defaultdict(int)
    
    for i in range(1, num_files+1):
        len_files = []
        for task in tasks:
            with open(f"{input_dir}/{task}/{i}.txt", "r") as f:
                content = f.read()
                content = content.split()
                len_files.append(len(content))
        average = sum(len_files)/len(len_files)

        # Process each file and accumulate counts
        for task in tasks:
            file_path = os.path.join(f"{input_dir}/{task}/", f"{i}.txt")
            pronouns = find_pronouns(lang, file_path, average)

            # Sum counts into combined_counts
            for pronoun, count in pronouns.items():
                combined_counts[pronoun] += count

    # Add combined counts to results dictionary with corpus as key
    results[corpus_name] = combined_counts

if __name__ == "__main__":
    corpus_list = GERMAN_CORPORA + ENGLISH_CORPORA
    results = {}  # Dictionary to store combined counts for each corpus

    for corpus in corpus_list:
        main(corpus, results)

    # Convert results dictionary to DataFrame
    df = pd.DataFrame(results).fillna(0).astype(int)  # Fill NaNs with 0 and cast to int
    df = df.T  # Transpose for each corpus to be a row

    # Save DataFrame as CSV
    output_csv_path = "../results/per_corpus/combined_pronoun_counts.csv"
    df.to_csv(output_csv_path, index=True)
    
    print(f"DataFrame saved to {output_csv_path}")
