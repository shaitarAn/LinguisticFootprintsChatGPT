# !/usr/bin/env python3
# -*- coding: utf8 -*-

'''This script will compare the number of connectives in chatGPT-written text with the number of connectives in human-written text. It will count the total number of connectives for English and German in the root directory. The list of connectives is from the tab-separated imported txt fils'''

import os
import pathlib
import csv
import re
from nltk import ngrams
import argparse
import spacy_udpipe
from collections import defaultdict
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config('config.yaml')

GERMAN_CORPORA = config['corpora']['german']
ENGLISH_CORPORA = config['corpora']['english']

# ############################################

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument('-o', '--output_dir', required=True, help="Directory where all results and outputs will go.")
parser.add_argument('-i', '--input_dir', required=True, help="Directory with generated data.")

args = parser.parse_args()

# ############################################

# Create a Path object for the directory
root = pathlib.Path(args.input_dir)

# check if output directory exists
if not os.path.exists('../results/connectives/'):
    os.makedirs('../results/connectives/')

def create_list_of_connectives(lang):
    # import the file of connectives from Thomas Meyer
    # the first column is the connective, the second column is the function, the third column is the frequency (if available)
    discourse_connectives_file = f'../../feature_extraction/resources/discourse_connectives_{lang.upper()}_Thomas_Meyer_2014.txt'
    # discourse_connectives_file = "../connectives_DE_frequency+20.txt"
    with open(discourse_connectives_file, 'r') as f:
        connectives = f.read().splitlines()
        connectives = [c.split('\t')[0].lower() for c in connectives]
        # print(connectives)
    return connectives

def make_ngrams(sentence, n):
    return ngrams(sentence, n)

def extract_connectives(language, corpus, system):
    nlp = spacy_udpipe.load(language)

    connectives = create_list_of_connectives(language)

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})
    file_dict = defaultdict(lambda: {'total': 0, 'capitalized': 0})

    directory_path = pathlib.Path(f"{root}/{corpus}/{system}")
    file_list = [file_path for file_path in directory_path.iterdir() if file_path.is_file()]

    for file_path in sorted(file_list):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()

            all_connectives = 0
            upper_connectives = 0

            doc = nlp(text)
            for sentence in doc.sents:
                tokens = [token.text for token in sentence]
                for n in range(4, 0, -1):
                    for ngram in make_ngrams(tokens, n):
                        ngram_text = ' '.join(ngram).lower()
                        if ngram_text in connectives:
                            key = 'capitalized' if ngram[0][0].isupper() else 'lower'
                            system_dict[ngram_text][key] += 1
                            all_connectives += 1
                            if key == 'capitalized':
                                upper_connectives += 1

            file_id = os.path.splitext(os.path.basename(file_path))[0]
            file_dict[file_id] = {'total': all_connectives, 'capitalized': upper_connectives}

    return dict(system_dict), dict(file_dict)

def main():

    for subdirectory in os.listdir(root):
        corpus_path = os.path.join(root, subdirectory)
        if not os.path.isdir(corpus_path):
            continue

        lang = 'de' if subdirectory in GERMAN_CORPORA else 'en'
        print(f"Processing {lang} corpus: {subdirectory}")

        spacy_udpipe.download(lang)

        system_dicts = {}

        for system in os.listdir(corpus_path):
            system_path = os.path.join(corpus_path, system)
            if not os.path.isdir(system_path):
                continue

            system_dicts[system], _ = extract_connectives(lang, subdirectory, system)

        combined_dict = {}
        for system, data in system_dicts.items():
            for key, counts in data.items():
                if key not in combined_dict:
                    combined_dict[key] = {}
                combined_dict[key].update({
                    f"{system}_upper": counts['capitalized'],
                    f"{system}_total": counts['capitalized'] + counts['lower']
                })

        csv_file_path = os.path.join(args.output_dir, 'results', 'connectives', f'connectives_all_{subdirectory}.csv')
        os.makedirs(os.path.dirname(csv_file_path), exist_ok=True)
        with open(csv_file_path, 'w', newline='') as f:
            fieldnames = ['connective']
            for system in system_dicts:
                fieldnames.extend([f"{system}_upper", f"{system}_total"])
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for key, values in combined_dict.items():
                row = {'connective': key}
                row.update(values)
                writer.writerow(row)

        print(f"Data written to {csv_file_path}")

# Example usage
if __name__ == "__main__":
    main()
    
# def main():

#     # itarate over subdirectories in directory_path
#     for subdirectory in os.listdir(root):
#         # itarate over files in subdirectory
#         corpus = subdirectory
#         if corpus in GERMAN_CORPORA:
#             lang = 'de'
#         else:
#             lang = 'en'
        
#         if not os.path.isdir(os.path.join(root, subdirectory)):
#                 continue 

#         print("-------------------")
#         # print(corpus)      

#         human_dict = {}
#         continue_dict = {} 
#         explain_dict = {}
#         create_dict = {} 
#         combined_dict = {} 
#         combined_file_dict = {}    

#         for system in os.listdir(os.path.join(root, subdirectory)):
    
#             print(lang, corpus, system)

#             if system == 'human':
#                 human_dict, human_file_dict = extract_connectives(lang, corpus, system)

#             elif system == 'continue':
#                 continue_dict, continue_file_dict = extract_connectives(lang, corpus, system)

#             elif system == 'explain':
#                 explain_dict, explain_file_dict = extract_connectives(lang, corpus, system)

#             elif system == 'create':
#                 create_dict, create_file_dict = extract_connectives(lang, corpus, system)
            
#             else:
#                 continue

#         # combine 4 dictionaries into one based on keys
#         for key in set(human_dict.keys()) | set(continue_dict.keys()) | set(explain_dict.keys()) | set(create_dict.keys()):
#             combined_dict[key] = {
#             'human_upper': human_dict.get(key, {}).get('capitalized', 0),
#             'human_total': human_dict.get(key, {}).get('capitalized', 0) + human_dict.get(key, {}).get('lower', 0),
#             'continue_upper': continue_dict.get(key, {}).get('capitalized', 0),
#             'continue_total': continue_dict.get(key, {}).get('capitalized', 0) + continue_dict.get(key, {}).get('lower', 0),
#             'explain_upper': explain_dict.get(key, {}).get('capitalized', 0),
#             'explain_total': explain_dict.get(key, {}).get('capitalized', 0) + explain_dict.get(key, {}).get('lower', 0),
#             'create_upper': create_dict.get(key, {}).get('capitalized', 0),
#             'create_total': create_dict.get(key, {}).get('capitalized', 0) + create_dict.get(key, {}).get('lower', 0),}

#         print(combined_dict)
#         print(combined_file_dict)

#         # write the dictionaries to csv files
#         with open(f'../results/connectives/connectives_all_{corpus}.csv', 'w') as f:
#             writer = csv.writer(f)
#             writer.writerow(['connective', 'human_upper', 'human_total', 'continue_upper', 'continue_total', 'explain_upper', 'explain_total', 'create_upper', 'create_total'])
#             for key, values in combined_dict.items():
#                 writer.writerow([key, values["human_upper"], values["human_total"], values["continue_upper"], values["continue_total"], values["explain_upper"], values["explain_total"], values["create_upper"], values["create_total"]])

# main()
