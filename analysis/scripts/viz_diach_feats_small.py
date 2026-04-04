import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import seaborn as sns
import pandas as pd
import os
import sys
from scipy.stats import ttest_ind
from scipy import stats

sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

language = "english"

def explore_features_interactively(path_to_data):

    sns.set(style="whitegrid")
    for metric, description in features_to_visualize_dict.items():
        try:
            df = load_data(metric, path_to_data)
            fig, ax = plt.subplots(figsize=(12, 6))
            plot_data(df, description, ax, 0)
            # plt.show()
        except FileNotFoundError:
            print(f"Feature {metric} not found for {language}")

def check_significance(p1, p2, feature):
    if stats.shapiro(p1)[1] < 0.05 and stats.shapiro(p2)[1] < 0.05:
        # print(f'Feature {feature} does not have a normal distribution for {p1} and {p2}')
        # if the null hypothesis is rejected, use the Mann-Whitney U test
        test = 'mannwhitneyu'
        statistic, pvalue = stats.mannwhitneyu(p1, p2, alternative='two-sided')
        if pvalue < 0.05:
            print(f'significant for {feature}', pvalue)

    else:
        # print(f'Feature {feature} has a normal distribution for {p1} and {p2}')
        # if the null hypothesis is not rejected, use the t-test
        test = 't-test'
        statistic, pvalue = ttest_ind(p1, p2)
        if pvalue < 0.05:
            print(f'significant for {feature}')

def load_data(metrics, path_to_data):
    file_paths = [
        os.path.join(path_to_data, f"2309gpt3/results/per_language/{language}", f"{metrics}.csv"),
        os.path.join(path_to_data, f"2403gpt4/results/per_language/{language}", f"{metrics}.csv")
    ]
    df_gpt3 = pd.read_csv(file_paths[0])
    df_gpt3['dataset'] = 'GPT3'
    df_gpt4 = pd.read_csv(file_paths[1])
    df_gpt4['dataset'] = 'GPT4'
    # add a column where the values for continue, explain, create are averaged
    df_gpt3['gpt-3'] = df_gpt3[['continue', 'explain', 'create']].mean(axis=1)
    df_gpt4['gpt-4'] = df_gpt4[['continue', 'explain', 'create']].mean(axis=1)
    # rename the columns
    df_gpt3 = df_gpt3.rename(columns={'human': 'human-gpt3'})
    combined_df = pd.concat([df_gpt3, df_gpt4], axis=1)
    # select only the columns we need
    combined_df = combined_df[['human', 'gpt-3', 'gpt-4']]

    # check for significance between the gpt-3 and gpt-4
    check_significance(combined_df['gpt-3'], combined_df['gpt-4'], metrics)

    return combined_df

import os
import pandas as pd

def load_data_lang(metrics, path_to_data):

    file_paths = [
        os.path.join(path_to_data, f"2309gpt3/results/per_language/english", f"{metrics}.csv"),
        os.path.join(path_to_data, f"2309gpt3/results/per_language/german", f"{metrics}.csv"),

        os.path.join(path_to_data, f"2403gpt4/results/per_language/english", f"{metrics}.csv"),
        os.path.join(path_to_data, f"2403gpt4/results/per_language/german", f"{metrics}.csv")
    ]
    
    # Load the data for both languages
    df_eng_3 = pd.read_csv(file_paths[0])
    df_ger_3 = pd.read_csv(file_paths[1])
    df_eng_4 = pd.read_csv(file_paths[2])
    df_ger_4 = pd.read_csv(file_paths[3])

    # concatenate the english and german dataframes for each generation
    df_3 = pd.concat([df_eng_3, df_ger_3], axis=0)
    df_4 = pd.concat([df_eng_4, df_ger_4], axis=0)

    # df_3['dataset'] = 'GPT3'
    # df_4['dataset'] = 'GPT4'

    # add a column where the values for continue, explain, create are averaged
    df_3['gpt-3'] = df_3[['continue', 'explain', 'create']].mean(axis=1)
    df_4['gpt-4'] = df_4[['continue', 'explain', 'create']].mean(axis=1)

    # rename the columns
    df_3 = df_3.rename(columns={'human': 'human-gpt3'})
    # df_4 = df_4.rename(columns={'human': 'human-gpt4'})
    combined_df = pd.concat([df_3, df_4], axis=1)

    print("combined_df.columns")
    print(combined_df.columns)
    # select only the columns we need
    combined_df = combined_df[['human', 'gpt-3', 'gpt-4']]

    return combined_df

def plot_data(df, metric, ax, i):
    # Melt the DataFrame from wide to long format
    melted_df = df.melt(var_name='group', value_name='score')

    colors = sns.color_palette('Set3', 12)
    # Check the language setting and apply the appropriate color palette
    selected_colors = [colors[0], colors[9], colors[11]]
    sns.boxplot(x='group', y='score', data=melted_df, palette=selected_colors, showfliers=False, ax=ax)

    # Set plot title and adjust font settings
    ax.set_title(metric, fontsize=20)

    # Set labels and formatting
    ax.set_xlabel('')
    ax.set_ylabel('')
    ax.tick_params(axis='x', labelsize=20, length=6)
    ax.tick_params(axis='y', labelsize=16)
    # Rotate x-tick labels for better readability
    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    # Remove the legend if it exists
    legend = ax.get_legend()
    if legend:
        legend.remove()

    # tight layout
    plt.tight_layout()

def main():
    path_to_data = "../../feature_extraction/"
    sns.set(style="whitegrid")

    feats_to_check_english = {
        "mtld": "MTLD",
        "pos_prop_PUNCT": "% Punctuation",
        "mean_word_length": "Avg Word Length",
        "lix": "LIX",
        "prop_adjacent_dependency_relation_mean": "% Adjacent Dep",
    }

    # feats_to_check_english = {
    # "flesch_reading_ease": "FRE",
    # # "flesch_kincaid_grade": "FKG",
    # "gunning_fog": "Gunning Fog",
    # "automated_readability_index": "ARI",
    # "coleman_liau_index": "CLI",
    # "lix": "LIX",
    # # "rix": "RIX",
    # }

    # # # other features to check
    # feats_to_check_english = {
    #     "proportion_unique_tokens": "% Unique Tokens",
    #     "mtld": "MTLD",
    #     "type_token_ratio": "TTR",
    #     "yules_k": "Yule's I",
    #     # "top_ngram_chr_fraction_3": "Top 3-Char",
    #     # "duplicate_ngram_chr_fraction_5": "5-Char Dupls",
    # }

    feats_to_check = feats_to_check_english

    with PdfPages(f'models_bothLang_small.pdf') as pdf:
        # Create a figure with 1 row and 5 columns of subplots
        fig, axes = plt.subplots(1, 5, figsize=(16, 4), constrained_layout=True)
        # Adjust horizontal spacing

        fig.subplots_adjust(wspace=0.1)
        
        # Iterate over the features and plot them
        for i, (metric, description) in enumerate(feats_to_check.items()):
            ax = axes[i]
            df = load_data_lang(metric, path_to_data)
            plot_data(df, description, ax, i)

        plt.show()  # Display the plot
        # pdf.savefig(fig)  # Save the figure to a PDF file
        
        # Save as PNG
        fig.savefig(f'models_{language}_small.png', dpi=300, bbox_inches='tight')
        # Save the figure to a PNG file
        plt.close(fig)

if __name__ == "__main__":
    main()
