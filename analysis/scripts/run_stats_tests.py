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
import yaml

# ########################################################################

# parse the input arguments
parser = argparse.ArgumentParser(description='Calculate the Benjamini-Hochberg correction for multiple hypothesis testing')
parser.add_argument('language', help='the language of the input files')
# add alpha to the parser
parser.add_argument('--alpha', '-a', type=float, default=0.05, help='the significance level (default: 0.05)')
# add the option to choose the method for multiple hypothesis testing correction
parser.add_argument('--method', '-m', choices=['bh', 'holm', 'bon'], default='bh', help='the method for multiple hypothesis testing correction (default: Benjamini-Hochberg)')
parser.add_argument('--config', '-c', required=True, help='Path to the configuration file.')
parser.add_argument('--input_dir', '-i', required=True, help='Path to the input directory.')

args = parser.parse_args()

language = args.language
alpha = args.alpha
method = args.method
generation_name = args.input_dir.split('/')[-2]

# ########################################################################

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

config = load_config(args.config)
domains = config['domains']
tasks = config['tasks']
# print(tasks)
# print(domains)

# ########################################################################

methods = {'bh': 'Benjamini-Hochberg', 'holm': 'Holm', 'bon': 'Bonferroni'}

def create_task_pairs(tasks):
    # Generate all combinations of task pairs
    return ["-".join(map(str, comb)) for comb in itertools.combinations(tasks, 2)]

def initialize_significant_features(task_pairs):
    return {pair: {'bon': [], 'bh': []} for pair in task_pairs}

task_pairs = create_task_pairs(tasks)
significant_features = initialize_significant_features(task_pairs)

# ########################################################################

def combine_means(dfp, input_dir, files):
    
    # initialize a dataframe with 5 columns: feature + tasks
    dfm = pd.DataFrame(columns=tasks)

    # create a list of only significant features, where the null hypothesis is rejected
    features_list = dfp[dfp['reject'] == True]['feature'].unique()
    # print(features_list[:5])

    # iterate over the significant features and add the data to the dataframe
    for file in files:
        feature = file.split('.')[0]
        if feature in features_list:
            # print(feature)
            feat = pd.read_csv(input_dir + file)
            # print(feat.head())
            # add the values to the dataframe
            dfm = pd.concat([dfm, feat], ignore_index=True)

    # print(dfm)
    # save the dataframe to a csv file
    # plot_means(f'../../viz/per_lang/{language}', dfm, f'{language} means')
    dfm.to_csv(f'../results/{generation_name}_{language}_SignFeats_{alpha}.csv', index=False)


def perform_multiple_test_correction(dfp):
        
    for p in dfp['persona'].unique():
        # p is a combination of two personas
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
        for p1, p2 in itertools.combinations(tasks, 2):
            # print(f'Feature {feature} for {p1} and {p2}')
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
    # print(files)

    # initialize a dataframe to store the feature, t-statistic, and p-value
    dfp = pd.DataFrame(columns=['feature', 'persona', 'test', 't-statistic', 'pvalue'])

    # control the normality of the distributions
    dfp = control_normality(dfp, input_dir, files)
    # print(dfp)

    # initialize the columns for the multiple hypothesis testing correction
    dfp['bon'] = np.nan
    dfp['bh'] = np.nan
    dfp['reject'] = np.nan

    # sort the dataframe by the p-value in ascending order
    dfp = dfp.sort_values(by='pvalue', ascending=True)
    # reset the index of the dataframe
    dfp = dfp.reset_index(drop=True)

    # perform the multiple hypothesis testing correction
    dfp = perform_multiple_test_correction(dfp)

    # plot_distribtuions(outputdir, dfp.pvalue, dfp.bon, language, language, method, alpha)
    combine_means(dfp, input_dir, files)

    return dfp


def main():

    # ######## run statistical analysis tests for each language ########

    input_dir = f'{args.input_dir}/per_language/{language}/'
    output_dir = '../../viz/per_lang'

    dfp = run_stats_tests(input_dir, output_dir)

    dfp.to_csv(f'../results/{generation_name}_{language}_stats_{alpha}.csv', index=False)

    with open(f'../results/{generation_name}_{language}_significant_features_{alpha}.json', 'w') as f:
        json.dump(significant_features, f)

    # print(language)
    # for p, v in significant_features.items():
    #     print(p, len(v['bon']))
    #     print(p, v['bon'])
    #     print()


    # ######## run statistical analysis tests for each domain ########

    for domain in domains:
        input_dir = f'{args.input_dir}/per_domain/{domain}/{language}/'
        output_dir = f'../../viz/per_domain/{domain}'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        dfp = run_stats_tests(input_dir, output_dir)
        
        dfp.to_csv(f'../results/{generation_name}_{language}_{domain}_stats_{alpha}.csv', index=False)
        with open(f'../results/{generation_name}_{language}_{domain}_significant_features_{alpha}.json', 'w') as f:
            json.dump(significant_features, f)

        # print(domain, language)
        # for p, v in significant_features.items():
        #     print(p, v['bon'])
        #     print()

    # ######## run statistical analysis tests on the combined language data ########

    english_input_dir = f'{args.input_dir}/per_language/english/'
    german_input_dir = f'{args.input_dir}/per_language/german/'

    output_dir = '../../viz/combo_lang'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files_en = os.listdir(english_input_dir)
    # files_de = os.listdir(german_input_dir)
    # print(files)

    # initialize a dataframe to store the feature, t-statistic, and p-value
    # Initialize a list to collect data
    data_entries = []

    for f in files_en:
        feature = f.split('.')[0]
        df_en = pd.read_csv(english_input_dir + f)
        try:
            df_de = pd.read_csv(german_input_dir + f)
        except:
            df_de = pd.DataFrame(columns=tasks)
        
        df_comb = pd.concat([df_en, df_de], axis=0)

        for p1, p2 in itertools.combinations(tasks, 2):
            if stats.shapiro(df_comb[p1])[1] < 0.05 and stats.shapiro(df_comb[p2])[1] < 0.05:
                test = 'mannwhitneyu'
                statistic, pvalue = stats.mannwhitneyu(df_comb[p1], df_comb[p2], alternative='two-sided')
            else:
                test = 't-test'
                statistic, pvalue = ttest_ind(df_comb[p1], df_comb[p2], equal_var=False) 

            data_entries.append({
                'feature': feature,
                'persona': f'{p1}-{p2}',
                'test': test,
                't-statistic': statistic,
                'pvalue': pvalue
            })

    # Convert list to DataFrame after the loop
    dfp2 = pd.DataFrame(data_entries)

    # initialize the columns for the multiple hypothesis testing correction
    dfp2['bon'] = np.nan
    dfp2['bh'] = np.nan
    dfp2['reject'] = np.nan

    # sort the dataframe by the p-value in ascending order
    dfp2 = dfp2.sort_values(by='pvalue', ascending=True)
    # reset the index of the dataframe
    dfp2 = dfp2.reset_index(drop=True)

    # perform the multiple hypothesis testing correction
    dfp2 = perform_multiple_test_correction(dfp2)

    # plot_distribtuions(outputdir, dfp.pvalue, dfp.bon, language, language, method, alpha)
    # combine_means(dfp, input_dir, files)

    # write the combined dataframe to a csv file
    dfp2.to_csv(f'../results/{generation_name}_english_german_stats_{alpha}.csv', index=False)

    with open(f'../results/{generation_name}_english_german_significant_features_{alpha}.json', 'w') as f:
        json.dump(significant_features, f)



if __name__ == "__main__":
    # pass
    main()



























































