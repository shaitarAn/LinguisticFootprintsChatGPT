import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind
# from scipy.stats import tukey_hsd
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
warnings.simplefilter(action='ignore', category=FutureWarning)
# Suppress the warning message
pd.set_option('mode.chained_assignment', None)
import sys
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_raw_counts

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

# initialize a dictionnary of significant features per persona
significant_features = {'human-continue':{'bon':[], 'bh':[]}, 'human-explain':{'bon':[], 'bh':[]}, 'human-create':{'bon':[], 'bh':[]}, 'continue-explain':{'bon':[], 'bh':[]}, 'continue-create':{'bon':[], 'bh':[]}, 'explain-create':{'bon':[], 'bh':[]}}


def plot_values(dfp, p):
        
    # drop the rows with NaN and None values in place
    dfp = dfp.dropna() 

    # sort the dataframe by the p-value in ascending order
    dfp = dfp.sort_values(by='pvalue', ascending=False)

    # plot the corrected p-values
    sns.set(style="whitegrid")
    # make scatter plot
    ax = sns.scatterplot(x="pvalue", y="feature", data=dfp, color='b', label='t-test p-values')
    # add a line for B-H correction q-values
    ax = sns.scatterplot(x=method, y="feature", data=dfp, color='g', label=f'{methods[method]} multiple testing correction')
    # increase the size of the plot
    fig = plt.gcf()
    fig.set_size_inches(15, 10)

    # change x-axis label
    plt.xlabel(f'feature significance for {p}')

    # add the alpha level to the plot in light gray
    plt.axvline(x=alpha, color='r', linestyle='--', label=f'alpha = {alpha}')
    # give more space to the y-axis labels
    plt.tight_layout()
    plt.savefig(f'../../viz/per_lang/{language}/{method}_{p}_{alpha}.pdf')
    # close the plot
    plt.close()

def main():

    input_dir = f'../../feature_extraction/results/per_language/{language}/'
    files = os.listdir(input_dir)

    # initialize a dataframe to store the feature, t-statistic, and p-value
    dfp = pd.DataFrame(columns=['feature', 'persona', 'test', 't-statistic', 'pvalue'])

    for f in files:
        feature = f.split('.')[0]
        df = pd.read_csv(input_dir + f)
        
        # iterate over all the personas and calculate the t-statistic and p-value
        personas = ['human', 'continue', 'explain', 'create']

        for p1, p2 in itertools.combinations(personas, 2):
            # check if both samples have a normal distribution
            # if both samples have a normal distribution, perform the t-test
            # if not, perform the Mann-Whitney U test
            if stats.shapiro(df[p1])[1] < 0.05 and stats.shapiro(df[p2])[1] < 0.05:
                print('parametric', feature, p1, p2)
                t_stat, p_value = ttest_ind(df[p1], df[p2], equal_var=False)
                dfp = dfp.append({'feature': feature, 'persona': f'{p1}-{p2}', 'test':'t', 't-statistic': t_stat, 'pvalue': p_value}, ignore_index=True)
            else:
                print('non-parametric', feature, p1, p2)
                t_stat, p_value = stats.mannwhitneyu(df[p1], df[p2], alternative='two-sided')
                dfp = dfp.append({'feature': feature, 'persona': f'{p1}-{p2}', 'test':'mannwhitneyu', 't-statistic': t_stat, 'pvalue': p_value}, ignore_index=True)

        print(f'Finished {feature}')

    # initialize the columns for the multiple hypothesis testing correction
    dfp['bon'] = np.nan
    dfp['bh'] = np.nan

    # sort the dataframe by the p-value in ascending order
    dfp = dfp.sort_values(by='pvalue', ascending=True)
    # reset the index of the dataframe
    dfp = dfp.reset_index(drop=True)
            
    # calculate the Benjamini-Hochberg correction for multiple hypothesis testing for each persona
    for p in dfp['persona'].unique():
        dfp_p = dfp[dfp['persona'] == p]

        # ############################################################
        # perform multiple hypothesis testing correction for each persona
        # ############################################################

        # method 1: Bonferroni correction
        bonferroni = dfp_p.pvalue * len(dfp_p)
        dfp_p['bon'] = bonferroni
        # add the Bonferroni correction to the main dataframe for this persona
        dfp.loc[dfp['persona'] == p, 'bon'] = dfp_p['bon']

        # method 2: Benjamini-Hochberg correction
        # reorder the p-values in ascending order
        dfp_p = dfp_p.sort_values(by='pvalue', ascending=True)
        # reset the index of the persona dataframe
        dfp_p = dfp_p.reset_index(drop=True)
        bh_values = dfp_p.pvalue * len(dfp_p) / (dfp_p.index + 1)
        dfp_p['bh'] = bh_values

        # add the Benjamini-Hochberg correction to the main dataframe for this persona
        dfp.loc[dfp['persona'] == p, 'bh'] = dfp_p['bh']

        # add the significant features to the dictionnary
        significant_features[p]['bh'] = dfp_p[dfp_p['bh'] < alpha]['feature'].tolist()
        significant_features[p]['bon'] = dfp_p[dfp_p['bon'] < alpha]['feature'].tolist()

        plot_values(dfp_p, p)

    # save the dataframe to a csv file
    dfp.to_csv(f'../results/{language}_stats_{alpha}.csv', index=False)

    # save the significant features to a json file
    with open(f'../results/{language}_significant_features_{alpha}.json', 'w') as f:
        json.dump(significant_features, f)

if __name__ == '__main__':
    main()






















































