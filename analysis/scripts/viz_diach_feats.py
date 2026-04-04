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

language = "german"

def explore_features_interactively(path_to_data):

    sns.set(style="whitegrid")
    for metric, description in features_to_visualize_dict.items():
        try:
            df = load_data(metric, path_to_data)
            fig, ax = plt.subplots(figsize=(10, 6))
            plot_data(df, description, ax, 0)
            plt.show()
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

    # combined_df = pd.concat([df_gpt3, df_gpt4])
    # print(combined_df)
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

    # Conditionally set x-labels and ticks based on subplot index
    if i < 6:  # Assuming 'i' specifies the subplot index and there are 5 plots per row
        ax.set_xlabel('')  # Clear x-label for top row subplots
        ax.tick_params(axis='x', labelsize=0, length=0)  # Hide x-tick labels and ticks for top row
    else:
        ax.set_xlabel('')  # Set x-label for bottom row subplots
        ax.tick_params(axis='x', labelsize=20, length=6)
        # rotate x-tick labels for better readability
        for tick in ax.get_xticklabels():
            tick.set_rotation(45)

    ax.set_ylabel('')
    ax.tick_params(axis='y', labelsize=16)

    # Remove the legend if it exists
    legend = ax.get_legend()
    if legend:
        legend.remove()


def main():
    path_to_data = "../../feature_extraction/"
    sns.set(style="whitegrid")
    # explore_features_interactively(path_to_data)

    feats_to_check_english = {
        "proportion_unique_tokens": "Unique Tokens",
        "mtld": "MTLD",
        # "type_token_ratio": "TTR",
        "yules_k": "Yule's I",
        "top_ngram_chr_fraction_3": "Top 3-Char",
        "sentence_length_mean": "Avg Sent Len",
        "sentence_length_std": "Sent Len StD",
        # "pos_prop_ADJ": "Adjectives",
        # "entropy": "Entropy",
        "pos_prop_CCONJ": "CCONJ",
        "pos_prop_SCONJ": "SCONJ",
        # "token_length_mean": "Average Token Length",
        "lix": "LIX",
        "flesch_kincaid_grade": "FKGL",
        "pos_prop_DET": "Determiners",
        "pos_prop_VERB": "Verbs",
    }

    feats_to_check_german = {
        # "sentence_length_mean": "Average Sentence Length",
        "proportion_unique_tokens": "Unique Tokens",
        "mtld": "MTLD",
        "type_token_ratio": "TTR",
        "yules_k": "Yule's I",
        # "top_ngram_chr_fraction_3": "Top 3-Char",
        "duplicate_ngram_chr_fraction_5": "5-Char Dupls",
        "duplicate_ngram_chr_fraction_9": "9-Char Dupls",
        # "dependency_distance_std": "Dependency Std",
        # "pos_prop_ADV": "Adverbs",
        "pos_prop_CCONJ": "CCONJ",
        "pos_prop_SCONJ": "SCONJ",
        # "pos_prop_PUNCT": "Punctuation",
        "first_order_coherence": "1st Ord Coherence",
        "sentence_length_std": "Sent Len StD",
        # "connectives_cap": "Connectives Capitalised",
        "entropy": "Entropy",
        "shannon_entropy": "Shannon",
        
    }

    feats_to_check = feats_to_check_english if language == "english" else feats_to_check_german

    with PdfPages(f'../../viz/for_paper/models_{language}.pdf') as pdf:
        # Create a figure with 2 rows and 5 columns of subplots
        fig, axes = plt.subplots(2, 6, figsize=(20, 8), constrained_layout=True)
        # Adjust horizontal and vertical spacing
        fig.subplots_adjust(hspace=0.2, wspace=0.1)  # Reduced hspace from 0.5 to 0.2
        # Remove plt.tight_layout() if using constrained_layout, as they can conflict
        # Iterate over the features and plot them
        for i, (metric, description) in enumerate(feats_to_check.items()):
            ax = axes[i // 6, i % 6]
            df = load_data(metric, path_to_data)
            plot_data(df, description, ax, i)

        plt.show()  # Display the plot
        pdf.savefig(fig)  # Save the figure to a PDF file
        plt.close(fig) 

if __name__ == "__main__":
    main()
