# script adapted from https://github.com/dimitarsh1/BiasMT/tree/main/scripts/diversity

# example call: python shannon_pairwise.py -f ~/switchdrive/IMAGINE_files/datasets/nodalida/wmt22/tokenized/wmt22_de_A.txt -l de -sys A_wmt22 -v freq_voc/wmt22_de_A.freq_voc -t 0 > results_shannon/all_mostfrequent_wmt22_de_A.txt
#
# writes the results at the end of diversity_scores.csv
# as: "system", "shannon", "simpson"
# and also Shannon's entropy per lemma in results_shannon/shannon_per_lemma_{sys}.csv

import statistics
import argparse
import os
import numpy as np
from scipy.stats import ttest_ind
from mosestokenizer import *
from biasmt_metrics import *
import spacy_udpipe
import sys
import time
import csv


def main():

    # print("Starting...")
    ''' main function '''
    # read argument - file with data
    parser = argparse.ArgumentParser(
        description='Extracts words to a dictionary with their frequencies.')
    parser.add_argument('-f', '--files', required=True, help='the files to read.', nargs='+')
    parser.add_argument('-l', '--language', required=True, help='the language.', default='en')
    parser.add_argument('-sys', '--system', required=False, help='the system.', default='original')
    parser.add_argument('-dat', '--dataset', required=False, help='the corpus.', default='dataset')
    parser.add_argument('-v', '--frequency-vocabulary', required=False,
                        help='a frequency vocabulary', default=None)
    parser.add_argument('-t', '--top-words', required=False,
                        help='number of words with top frequencies.', default='1000')

    parser.add_argument('-i', '--iterations', required=False,
                        help='the number of iterations for the bootstrap.', default='1000')
    parser.add_argument('-s', '--sample-size', required=False,
                        help='the sample size (in sentences).', default='100')
    parser.add_argument('-o', '--output_dir', required=True, help="Directory where all results and outputs will go.")

    args = parser.parse_args()

    lang = args.language

    spacy_udpipe.download(lang)

    freq_dict = []
    if args.frequency_vocabulary is not None:
        with open(args.frequency_vocabulary, "r") as iF:
            all_lines = iF.readlines()
            top = int(args.top_words) if (int(args.top_words) < len(
                all_lines) and int(args.top_words) > 0) else len(all_lines)
            freq_dict = [line.strip().split()[0] for line in all_lines[:top]]
    else:
        freq_dict = None

    if freq_dict is not None:
        print("Frequency Dictionary size: " + str(len(freq_dict)))

    sentences = {}

    metrics_bs = {}

    # 1. read all the file
    for textfile in args.files:
        system = args.system
        # system = os.path.splitext(os.path.basename(textfile))[0]
        sentences[system] = []
        # print(textfile)
        with open(textfile, 'r') as ifh:
            # ifh = csv.reader(ifh, delimiter=",")
            # next(ifh)
            
            # ! Spacy UDPIPE crashes if we keep also empty lines
            sentences[system] = [s.strip() for s in ifh.readlines() if s.strip()]
            # sentences[system] = [s[1].strip() for s in ifh if s.strip()]

    # print(sentences)
    # 2. Compute overall metrics and per-lemma shannon scores

    file_exists = os.path.isfile(f"{args.output_dir}/results/morphology/{args.dataset}.csv")

    with open(f"{args.output_dir}/results/morphology/{args.dataset}.csv", 'a', newline='') as outf:
        writer1 = csv.writer(outf, delimiter=',')

        if not file_exists:
            writer1.writerow(["system", "file", "shannon", "simpson"])

        for syst in sentences:
            # Split the file name using underscore as the delimiter
            parts = syst.split("_")

            # Extract the first part
            author = parts[0]
            rest = "_".join(parts[1:])
            # check if the output folder exists
            if not os.path.exists(f"{args.output_dir}/morphology/per_lemma/{args.dataset}"):
                os.makedirs(f"{args.output_dir}/morphology/per_lemma/{args.dataset}")
            with open(f"{args.output_dir}/morphology/per_lemma/{args.dataset}/{syst}.csv", "w") as outf2:
                print(syst)
                                
                score = compute_gram_diversity(sentences[syst], args.dataset, lang, syst, freq_dict)
                # Shannon entropy, (removed invSimpDiv from output ) , Simpson's diversity
                writer1.writerow([author, rest, round(score[2]*100, 2), round(score[0]*100, 2)])

                # file containing shannon scores per lemma 
                writer2 = csv.writer(outf2, delimiter=',')
                writer2.writerow(["lemma", "shannon"])              
                for k, v in score[3].items():
                    writer2.writerow([k, v])
            
                # print(" & ".join([str(s) for s in score]))
                # print([])



    sys.exit("Done")


if __name__ == "__main__":
    main()
