#!/usr/bin/python3
# -*- coding: utf-8 -*-

# scripts adapted from https://github.com/dimitarsh1/BiasMT/tree/main/scripts/diversity

''' Computes the pairwise lexical diversity standard metrics: TTR, inverse Yules, MTLD
'''
import argparse
import os
import sys
import csv
import numpy as np
from scipy.stats import ttest_ind
from mosestokenizer import *
from biasmt_metrics import *
       
def compute_significance(metrics, iterations):
    ''' Compute pairwise significance interval

        :param metrics: dictionary with systems and metrics
        :param iterations: the number of iterations
        :returns: a socre (float)
    '''
    # now, we are able to compute statistical significance
    # print('delta(xi) > delta(x):')
    scores = {}
    for system1 in metrics:
        scores[system1] = {}
        for system2 in metrics:
            s = 0.0
            for i in range(iterations):
                if round(metrics[system1][i]*1000, 4) > round(metrics[system2][i]*1000, 4):
                    s += 1.0
            if system1 == system2:
                scores[system1][system2] = -1.0
            else:
                scores[system1][system2] = s / iterations
    return scores
    

def compute_ttest_scikit(metrics, iterations):
    ''' Compute pairwise significance interval

        :param metrics: dictionary with systems and metrics
        :param iterations: the number of iterations
        :returns: a socre (float)
    '''
    scores = {}
    print('\nScikit ttest:')
    for system1 in metrics:
        scores[system1] = {}
        for system2 in metrics:
            t, p =  ttest_ind(metrics[system1], metrics[system2])
            scores[system1][system2] = p
        
    return scores


def print_latex_table(scores, metric_title):
    ''' Prints a table in latex format; ready to incorporate into a tex file
        :param scores: dictionary with scores and systems
        :param metric_title: identifying the metric (string)
    '''
    print(' '.join([str(s) for s in scores.keys()]))
    for system in scores:
        print(system + ' ' + ' '.join([str(p) for p in scores[system].values()]))

    print('\n')
    print('  & ' + ' & '.join([str(s) for s in scores[system].keys()]) + '\\\\\hline')
    for system in scores:
        print_en = False
        print(system, end='')
        for system2 in scores:
            p = scores[system][system2]
            if (p >= 0.0 and p < 0.05) or p >= 0.95:
                if print_en:
                    print(' & Y', end='')
                else:
                    print(' & ', end='')
            else:
                if print_en:
                    print(' & N', end='')
                else:
                    print(' & ', end='')

            if system == system2:
                print_en = True
        print('\\\\\hline')

def main():
    ''' main function '''
    # read argument - file with data
    parser = argparse.ArgumentParser(description='Computes the pairwise lexical diversity standard metrics (TTR, inverse Yules, MTLD).')
    parser.add_argument('-f', '--files', required=True, help='the files to read.', nargs='+')
    # parser.add_argument('-l', '--language', required=False, help='the language.', default='en')
    parser.add_argument('-i', '--iterations', required=False, help='the number of iterations for the bootstrap.', default='1000')
    parser.add_argument('-s', '--sample-size', required=False, help='the sample size (in sentences).', default='100')
    parser.add_argument('-g', '--stat-sign', required=False, action='store_true', help='Statistical significance (in sentences).', default=False)
    parser.add_argument('-o', '--outfile', type=str, required=True, help='The name of the output CSV file')
    parser.add_argument('-sys', '--persona', type=str, required=False, help='The name of the persona')

    
    args = parser.parse_args()
    persona = args.persona

    sentences = {}
    metrics = {'TTR':'compute_ttr', 'Yules': 'compute_yules_i', 'MTLD':'compute_mtld'}
    metrics_bs = {}
    
    length = 0
    
    # 1. read all the file
    for textfile in args.files:
        system = os.path.basename(textfile)
        print(system, file=sys.stderr)
        sentences[system] = []
        
        with open(textfile, 'r') as ifh:
            sentences[system] = [s.strip() for s in ifh.readlines()]
        
        if length == 0:
            length = len(sentences[system])
        
    # 2. Compute overall metrics
    scores = {}
    for metric in metrics:
        scores[metric] = {}
        for syst in sentences:
            # print("for system in sentences")
            # print(syst, file=sys.stderr)
            scores[metric][syst] = eval(metrics[metric])(sentences[syst])
            # print(metric, scores[metric][syst], file=sys.stderr)

    with open(args.outfile, 'a') as file:
        writer = csv.writer(file)
        # Write the headers only if the file does not exist or is empty
        if not os.path.exists(args.outfile) or os.path.getsize(args.outfile) == 0:
            writer.writerow(["system", "file", "TTR", "Yules", "MTLD"])
        for syst in sentences:
            writer.writerow([persona, syst, round(scores['TTR'][syst]*100,2), round(scores['Yules'][syst]*100,2), round(scores['MTLD'][syst],2)])

        # print('{},{},{},{}'.format(syst,round(scores['TTR'][syst]*100,2),round(scores['Yules'][syst]*100,2),round(scores['MTLD'][syst],2)), file=sys.stdout)
        
    if not args.stat_sign:
        sys.exit("Done. No statistical significance")

    # # 3. read the other variables.
    # iters = int(args.iterations)
    # sample_size = int(args.sample_size)
    # sample_idxs = np.random.randint(0, length, size=(iters, sample_size))

    # # 4. Compute Sample metric
    # for metric in metrics:
    #     metrics_bs[metric] = {}
    #     for syst in sentences:
    #         metrics_bs[metric][syst] = compute_ld_metric(metrics[metric], sentences[syst], sample_idxs, iters)

    # for metric in metrics:
    #     print("-------------------------------------------------")
    #     print(metric)
    #     sign_scores = compute_significance(metrics_bs[metric], iters)
    #     print_latex_table(sign_scores, metric)
    #     sign_scores = compute_ttest_scikit(metrics_bs[metric], iters)
    #     print_latex_table(sign_scores, metric)
        
if __name__ == "__main__":
    main()
