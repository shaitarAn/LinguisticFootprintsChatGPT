import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind
import itertools
import numpy as np
import os
import json
import scikit_posthocs as sp
import seaborn as sns
import matplotlib.pyplot as plt
from statsmodels.stats.multitest import multipletests
import argparse 
import warnings
warnings.simplefilter(action='ignore')
# Suppress the warning message
pd.set_option('mode.chained_assignment', None)
import sys
from viz_helper import *

# parse the input arguments
parser = argparse.ArgumentParser(description='Calculate the Benjamini-Hochberg correction for multiple hypothesis testing')
parser.add_argument('language', help='the language of the input files')
# add alpha to the parser
parser.add_argument('--alpha', '-a', type=float, default=0.05, help='the significance level (default: 0.05)')
# add the option to choose the method for multiple hypothesis testing correction
parser.add_argument('--method', '-m', choices=['bh', 'holm', 'bon'], default='bh', help='the method for multiple hypothesis testing correction (default: Benjamini-Hochberg)')

args = parser.parse_args()

language = args.language
alpha = args.alpha
method = args.method

methods = {'bh': 'Benjamini-Hochberg', 'holm': 'Holm', 'bon': 'Bonferroni'}
domains = {'news': ['cnn', '20min', 'cs_en', 'cs_de'], 'scholar':['pubmed_en', 'pubmed_de', 'zora_de', 'zora_en'], 'clinical': ['e3c', 'ggponc']}

# initialize a dictionnary of significant features per persona
significant_features = {'human-continue':{'bon':[], 'bh':[]}, 'human-explain':{'bon':[], 'bh':[]}, 'human-create':{'bon':[], 'bh':[]}, 'continue-explain':{'bon':[], 'bh':[]}, 'continue-create':{'bon':[], 'bh':[]}, 'explain-create':{'bon':[], 'bh':[]}}

def combine_means(outputdir, dfp, input_dir, files):
    # initialize a dataframe with 5 columns: feature, human, continue, explain, create
    dfm = pd.DataFrame(columns=['human', 'continue', 'explain', 'create'])

    # create a list of the significant features
    features_list = dfp[dfp['reject'] == True]['feature'].unique()

    # iterate over the significant features and add the data to the dataframe
    for file in files:
        feature = file.split('.')[0]
        if feature in features_list:
            feat = pd.read_csv(input_dir + file)
            # add the values to the dataframe
            dfm = pd.concat([dfm, feat], ignore_index=True)

    # plot the means for each feature
    # plot_means(outputdir, dfm, language, alpha)

    # save the dataframe to a csv file
    dfm.to_csv(f'../results/{language}_means_{alpha}.csv', index=False)


def perform_multiple_test_correction(outputdir, dfp):
        
    for p in dfp['persona'].unique():
        dfp_p = dfp[dfp['persona'] == p]

        # ############################################################
        # perform multiple hypothesis testing correction for each persona pair
        # ############################################################

        # reorder the p-values in ascending order
        dfp_p = dfp_p.sort_values(by='pvalue', ascending=True)

        # method 1: Bonferroni correction
        # bonferroni = dfp_p.pvalue * len(dfp_p)
        reject, bonferroni, _, alpha_corrected = multipletests(dfp_p.pvalue, alpha=alpha, method='bonferroni', is_sorted=True, returnsorted=True)
        dfp_p['bon'] = bonferroni
        dfp_p['reject'] = reject
        # add the Bonferroni correction to the main dataframe for this persona
        dfp.loc[dfp['persona'] == p, 'bon'] = dfp_p['bon']
        dfp.loc[dfp['persona'] == p, 'reject'] = dfp_p['reject']
        # add the significant features to the dictionnary

        # print(p, alpha_corrected)
        # print(np.sum(reject))
        # print(reject)
        # print(dfp_p[reject])
        # print()

        # method 2: Benjamini-Hochberg correction
        # reset the index of the persona dataframe
        dfp_p = dfp_p.reset_index(drop=True)
        bh_values = dfp_p.pvalue * len(dfp_p) / (dfp_p.index + 1)
        # reject, bh_values, _, _ = multipletests(dfp_p.pvalue, alpha=alpha, method='fdr_bh', is_sorted=True, returnsorted=True)
        dfp_p['bh'] = bh_values

        # add the Benjamini-Hochberg correction to the main dataframe for this persona
        dfp.loc[dfp['persona'] == p, 'bh'] = dfp_p['bh']

        # add the significant features to the dictionnary
        significant_features[p]['bh'] = dfp_p[dfp_p['bh'] < alpha]['feature'].tolist()
        significant_features[p]['bon'] = dfp_p[dfp_p['bon'] < alpha]['feature'].tolist()

        # plot_values(outputdir, dfp_p, p, language, method, alpha)
        # plot_distribtuions(outputdir, dfp_p.pvalue, bonferroni, p, language, method, alpha)

    return dfp

def control_normality(dfp, input_dir, files):
    
    for f in files:
        feature = f.split('.')[0]
        df = pd.read_csv(input_dir + f)

        # iterate over all the personas and calculate the t-statistic and p-value
        personas = ['human', 'continue', 'explain', 'create']

        for p1, p2 in itertools.combinations(personas, 2):
            # check if both samples have a normal distribution
            # null hypothesis: the sample has a normal distribution
            if stats.shapiro(df[p1])[1] < 0.05 and stats.shapiro(df[p2])[1] < 0.05:
                # print(f'Feature {feature} does not have a normal distribution for {p1} and {p2}')
                # if the null hypothesis is rejected, use the Mann-Whitney U test
                test = 'mannwhitneyu'
                statistic, pvalue = stats.mannwhitneyu(df[p1], df[p2], alternative='two-sided')
                # update the dataframe with the t-statistic and p-value
                dfp = dfp.append({'feature': feature, 'persona': f'{p1}-{p2}', 'test':test, 't-statistic': statistic, 'pvalue': pvalue}, ignore_index=True)

            else:
                # print(f'Feature {feature} has a normal distribution for {p1} and {p2}')
                # if the null hypothesis is not rejected, use the t-test
                test = 't-test'
                statistic, pvalue = ttest_ind(df[p1], df[p2])
                # update the dataframe with the t-statistic and p-value
                dfp = dfp.append({'feature': feature, 'persona': f'{p1}-{p2}', 'test': test, 't-statistic': statistic, 'pvalue': pvalue}, ignore_index=True)

    return dfp

def run_stats_tests(input_dir, outputdir):
    
    files = os.listdir(input_dir)

    # initialize a dataframe to store the feature, t-statistic, and p-value
    dfp = pd.DataFrame(columns=['feature', 'persona', 'test', 't-statistic', 'pvalue'])

    # control the normality of the distributions
    dfp = control_normality(dfp, input_dir, files)

    # initialize the columns for the multiple hypothesis testing correction
    dfp['bon'] = np.nan
    dfp['bh'] = np.nan
    dfp['reject'] = np.nan

    # sort the dataframe by the p-value in ascending order
    dfp = dfp.sort_values(by='pvalue', ascending=True)
    # reset the index of the dataframe
    dfp = dfp.reset_index(drop=True)

    # perform the multiple hypothesis testing correction
    dfp = perform_multiple_test_correction(outputdir, dfp)

    # plot_distribtuions(outputdir, dfp.pvalue, dfp.bon, language, language, method, alpha)
    combine_means(outputdir, dfp, input_dir, files)

    return dfp


def main():

    # ######## run statistical analysis tests for each language ########

    input_dir = f'../../feature_extraction/results/per_language/{language}/'
    output_dir = '../../viz/per_lang'

    dfp = run_stats_tests(input_dir, output_dir)

    dfp.to_csv(f'../results/{language}_stats_{alpha}.csv', index=False)

    with open(f'../results/{language}_significant_features_{alpha}.json', 'w') as f:
        json.dump(significant_features, f)

    # print(language)
    # for p, v in significant_features.items():
    #     print(p, len(v['bon']))
    #     print(p, v['bon'])
    #     print()


    # ######## run statistical analysis tests for each domain ########

    for domain in ['news', 'science', 'clinical']:
        input_dir = f'../../feature_extraction/results/per_domain/{domain}/{language}/'
        output_dir = f'../../viz/per_domain/{domain}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        dfp = run_stats_tests(input_dir, output_dir)
        
        dfp.to_json(f'../results/{language}_{domain}_stats_{alpha}.json', orient='records')
        with open(f'../results/{language}_{domain}_significant_features_{alpha}.json', 'w') as f:
            json.dump(significant_features, f)

        # print(domain, language)
        # for p, v in significant_features.items():
        #     print(p, v['bon'])
        #     print()


if __name__ == "__main__":
    main()



























































