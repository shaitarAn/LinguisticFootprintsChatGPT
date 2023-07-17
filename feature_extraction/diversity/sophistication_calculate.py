# scripts adapted from https://github.com/dimitarsh1/BiasMT/tree/main/scripts/diversity

# example call:  python lexical_profile.py -f wmt22_de_A.txt wmt22_de_B.txt wmt22_en2de_bing.txt wmt22_en2de_deepl.txt wmt22_en2de_google.txt wmt22_en2de_pons.txt > lfp_wmt22.txt
# writes the lexical profile (frequency bands with step=1000 and last=2000) of each file to standard output
# output format: "system,B1,B2,B3" e.g. "wmt22_de_A,75.65,7.65,16.7"

import codecs
import statistics
import argparse
import os
import numpy as np
from scipy.stats import ttest_ind
from mosestokenizer import *
from biasmt_metrics import *
import sys
import csv
import time


def main():
    ''' main function '''
    # read argument - file with data
    parser = argparse.ArgumentParser(description='Computes the lexical profile.')
    parser.add_argument('-f', '--files', required=True,
                        help='the files to read (min 1).', nargs='+')
    parser.add_argument('-o', '--outfile', type=str, required=True, help='The name of the output CSV file')
    parser.add_argument('-sys', '--system', type=str, required=True, help='The name of the system')

    args = parser.parse_args()

    system = args.system

    sentences = {}

    settings = {'1000-2000-rest': (1000, 2000)} #, '100-to-2000-rest': (100, 2000), '500-to-2000-rest': (500, 2000)}
    
    metrics_bs = {}

    # 1. read all the file
    for textfile in args.files:
        # system = os.path.splitext(os.path.basename(textfile))[0]
        sentences[system] = []

        with codecs.open(textfile, 'r', 'utf8') as ifh:
            # ! Spacy UDPIPE crashes if we keep also empty lines
            sentences[system] = [s.strip() for s in ifh.readlines() if s.strip()]

    #print(sentences)
    # 2. Compute overall metrics
    with open(args.outfile, 'a') as oF:
        writer = csv.writer(oF)
        # Write the headers only if the file does not exist or is empty
        if not os.path.exists(args.outfile) or os.path.getsize(args.outfile) == 0:
            writer.writerow(["System", "B1", "B2", "B3"])
        for syst in sentences:
            # print("SYST", syst)
            for sett in settings:
                (step, last) = settings[sett]
                a = time.time()
                # print(syst, end=",")
                score = textToLFP(sentences[syst], step, last)
                print("Step: " + str(step) + " Last: " + str(last))
                print(",".join([str(round(s*100, 2)) for s in score]))
                results = [str(round(s*100, 2)) for s in score]
                results.insert(0, syst)
                writer.writerow(results)

    sys.exit("Done")


if __name__ == "__main__":
    main()
