# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import spacy
import os
import re
import argparse
import textdescriptives as td
import spacy_udpipe
from nltk import ngrams
from collections import defaultdict
from config import GERMAN_CORPORA, ENGLISH_CORPORA, tasks

'''
writes results to ..results/per_corpus
'''

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument('-o', '--output_dir', required=True, help="Directory where all results and outputs will go.")
parser.add_argument('-i', '--input_dir', required=True, help="Directory with generated data.")

args = parser.parse_args()

spacy_udpipe.download("en")
spacy_udpipe.download("de")

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('textdescriptives/all')

Dnlp = spacy.load('de_core_news_lg')
Dnlp.add_pipe('textdescriptives/all')

german_vowels = "aeiouäöüAEIOUÄÖÜ"
german_diphthongs = ['ai', 'au', 'ei', 'eu', 'äu', 'ie', 'ue']

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

def extract_connectives(language, file_name, average):
    
    # download the spacy model
    nlp = spacy_udpipe.load(language)

    # initialise a list of connectives from Thomas Meyer
    connectives = create_list_of_connectives(language)

    system_dict = defaultdict(lambda: {'lower': 0, 'capitalized': 0})

    # iterate through the files in the human-written directory with the language

    with open(file_name, 'r') as f:
        text = f.read()
        # print(len(text.split()))
        # cut the text to the average number of tokens
        if len(text.split()) > average:
            text = " ".join(text.split()[:int(average)])
        # print(average, len(text.split()))
        all_connectives = 0
        upper_connectives = 0

        # tokenize text with spacy_udpipe
        doc = nlp(text)
        for sentence in doc.sents:
            sentence = [token.text for token in sentence]
            # iterate through 4-grams, 3-grams, bigrams and unigrams in the sentence and count the number of connectives from the list
            for n in range(4, 0, -1):
                for ngram in make_ngrams(sentence, n):
                    ngram = ' '.join(ngram)

                    if ngram.lower() in connectives and ngram[0].isupper():
                        if ngram.lower() in system_dict and system_dict[ngram.lower()]["capitalized"] != 0:
                            system_dict[ngram.lower()]["capitalized"] += 1
                        else:
                            system_dict[ngram.lower()]["capitalized"] = 1
                        all_connectives += 1
                        upper_connectives += 1
                            
                    elif ngram.lower() in connectives and ngram[0].islower():
                        if ngram.lower() in system_dict and system_dict[ngram.lower()]["lower"] != 0:
                            system_dict[ngram.lower()]["lower"] += 1
                        else:
                            system_dict[ngram.lower()]["lower"] = 1
                        all_connectives += 1

    return system_dict

def process_file(file_path, lang, average):
    with open(file_path, 'r') as file:
        content = file.read()
        # cut the text to the average number of tokens
        if len(content.split()) > average:
            content = " ".join(content.split()[:int(average)])
        if lang == 'en':
            doc = nlp(content)
        elif lang == 'de':
            doc = Dnlp(content)
        
    return td.extract_dict(doc), doc

def count_oov_words(doc, system, corpus_name):
    if not os.path.exists(f"{args.output_dir}/results/oov/"):
        os.makedirs(f"{args.output_dir}/results/oov/")
    with open(f"{args.output_dir}/results/oov/{corpus_name}_{system}.txt", "a") as f:
        for token in doc:
            if token.is_oov:
                f.write(token.text.strip()+"\n")

def calculate_german_flesch_reading_ease(file_content):

    doc = Dnlp(file_content)
    # count the number of sentences in the text
    num_sentences = len(list(doc.sents))
    # count the number of words in the text
    num_words = sum(1 for token in doc if token.is_alpha)
    # count the number of vowels in the text
    total_vowels = len(re.findall(r'[aeiouäöü]', doc.text.lower()))
    # count the number of diphthongs in the text
    diphtongs = len(re.findall(r'ai|au|ei|eu|äu|ie|ue', doc.text.lower()))
    # # count the number of syllables in the text

    total_syllables = total_vowels - diphtongs
    flesch_reading_ease = 180-(num_words/num_sentences)- (58.5*(total_syllables/num_words))

    return flesch_reading_ease

def main(corpus):

    corpus_name = corpus.split("/")[-1]
    if corpus_name in ENGLISH_CORPORA:
        lang = 'en'
    else:
        lang = 'de'

    input_dir = os.path.join(args.input_dir, corpus)


    num_files = len(os.listdir(f"{input_dir}/human"))
    # print(corpus, num_files)
    
    for i in range(1, num_files+1):
        system_dataframes = []
        print(i)
        len_files = []
        for task in tasks:
            with open(f"{input_dir}/{task}/{i}.txt", "r") as f:
                content = f.read()
                # replace multiple spaces with a single space
                content = content.split()
                len_files.append(len(content))
                # print(task, system, i, len(content))
        average = sum(len_files)/len(len_files)
        # print(average)
        # print("--------------")

        for task in tasks:

            with open(f"{input_dir}/{task}/{i}.txt", "r") as f:
                print(task)
                file_content = f.read()

                file_path = os.path.join(f"{input_dir}/{task}/", f"{i}.txt")

                connectives = extract_connectives(lang, file_path, average)
                total_connectives = sum([connectives[key]['lower'] + connectives[key]['capitalized'] for key in connectives])
                uppper_connectives = sum([connectives[key]['capitalized'] for key in connectives])

                feature_values_list, obj = process_file(file_path, lang, average)
                count_oov_words(obj, task, corpus_name)

                df = pd.DataFrame()
                
                for feature_values in feature_values_list:
                    # convert the dictionary to a dataframe
                    feature_df = pd.DataFrame.from_dict(feature_values, orient='index')
                    df = pd.concat([df, feature_df], axis=1)
                    print(df)
                    # transpose the dataframe
                    df = df.transpose()

                # add a column with the number of connectives
                df['connectives'] = total_connectives
                df['connectives_cap'] = uppper_connectives

                print(df.head())

                # calculate the Flesch reading ease for German texts
                if lang == 'de':
                    flesch_reading_ease = calculate_german_flesch_reading_ease(file_content)
                    df['flesch_reading_ease'] = flesch_reading_ease

                #  drop column "text"
                df.drop(columns=['text'], inplace=True)
                # df.to_csv(output_truncated_file, index=False)

                #  transpose the dataframe 
                df = df.transpose()               
                df.columns = [task]
                # print(df.head())

                system_dataframes.append(df)  # Append the DataFrame to system_dataframes

        combined_dataframe = pd.concat(system_dataframes, axis=1)

        print(combined_dataframe.head())
        if not os.path.exists(f"{args.output_dir}/results/per_corpus/{corpus_name}"):
            os.makedirs(f"{args.output_dir}/results/per_corpus/{corpus_name}")

        # Step 4: Write the resulting dataframe to a CSV file
        combined_dataframe.to_csv(f"{args.output_dir}/results/per_corpus/{corpus_name}/{i}.csv", index=True)


if __name__ == "__main__":
    corpus_list = GERMAN_CORPORA + ENGLISH_CORPORA
    for corpus in corpus_list:
        main(corpus)