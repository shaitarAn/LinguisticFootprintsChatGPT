import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import seaborn as sns
from matplotlib import gridspec
from matplotlib.backends.backend_pdf import PdfPages
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

# === Configuration ===
GENERATION = "2403gpt4"  # Options: "2403gpt4" or "2309gpt3"

FEATURE_CATEGORIES = {
    "lexical_density": ["pos_prop_NOUN", "pos_prop_VERB", "pos_prop_ADJ", "pos_prop_ADV", "pos_prop_PRON"],
    "readability": ["flesch_reading_ease", "flesch_kincaid_grade", "coleman_liau_index", "automated_readability_index", "lix"],
    "syntax": ["dependency_distance_mean", "dependency_distance_std", "prop_adjacent_dependency_relation_mean",
               "prop_adjacent_dependency_relation_std", "first_order_coherence"],
    "descriptives": ["mean_word_length", "token_length_mean", "proportion_unique_tokens", "sentence_length_mean", "sentence_length_std"],
    "custom": ["mtld", "pos_prop_PUNCT", "mean_word_length", "lix", "sentence_length_std"]
}
WHAT_TO_VISUALIZE = "syntax"

# Select features for visualization
english_features = german_features = FEATURE_CATEGORIES[WHAT_TO_VISUALIZE]

# Set up a PDF file to save the plots
pdf_path = f"../../viz/{GENERATION}_{WHAT_TO_VISUALIZE}.pdf"
pdf_pages = PdfPages(pdf_path)

def viz_persona_features():
    # Create a figure
    fig = plt.figure(figsize=(20, 8))
    # Add a title
    # fig.suptitle('Comparison of English and German features', fontsize=16)

    # Add a grid
    gs = gridspec.GridSpec(2, 5, width_ratios=[1, 1, 1, 1, 1], height_ratios=[1, 1])

    # Add the English features
    for i, feature in enumerate(english_features):
        # import the data into a dataframe
        df = pd.read_csv(f'../../feature_extraction/{GENERATION}/results/per_language/english/{feature}.csv')
        ax = fig.add_subplot(gs[0, i])
        sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
        ax.set_title(' '.join(features_to_visualize_dict[feature].split(" ")[1:]), fontsize=20)
        ax.tick_params(axis='y', labelsize=14)  # Use tick_params to adjust y-axis labels
        # remove x-axis label
        ax.set_xlabel('')   
        ax.set_ylabel('')
        # remove ax.tick_params(axis='x) to remove x-tick labels

        
        if i == 0:
            ax.set_ylabel('English', fontsize=22)

    # Add the German features
    for i, feature in enumerate(german_features):
        # import the data into a dataframe
        df = pd.read_csv(f'../../feature_extraction/{GENERATION}/results/per_language/german/{feature}.csv')
        ax = fig.add_subplot(gs[1, i])
        sns.boxplot(data=df, palette='Set3', showmeans=True, ax=ax)
        ax.set_title('')
        ax.tick_params(axis='y', labelsize=14)
        # enlarge x-axis labels
        ax.tick_params(axis='x', labelsize=16, rotation=45)
        ax.set_ylabel('')
        if i == 0:
            ax.set_ylabel('German', fontsize=22)

    # Adjust layout to reduce margins
    plt.subplots_adjust(left=0.05, right=0.98, top=0.9, bottom=0.1)

    # save plot as ong
    # plt.savefig(f"../../viz/{generation}_{what_to_visualize}.png")

    # Save the figure to the pdf
    # pdf_pages.savefig(fig)
    # show the plot
    # plt.show()

    # Close the pdf
    pdf_pages.close()

# ##############

def plot_feature(feature, i, ax=None):
    try:
        # Import data
        df_gm = pd.read_csv(f'../../feature_extraction/{GENERATION}/results/per_language/german/{feature}.csv')
        df_en = pd.read_csv(f'../../feature_extraction/{GENERATION}/results/per_language/english/{feature}.csv')

        # Prepare data
        df_gm['Language'] = 'German'
        df_en['Language'] = 'English'
        df_gm['GPT-4'] = df_gm[['continue', 'explain', 'create']].mean(axis=1)
        df_en['GPT-4'] = df_en[['continue', 'explain', 'create']].mean(axis=1)

        # Melt dataframes for boxplot
        df_gm_melted = df_gm.melt(id_vars=['Language'], value_vars=['human', 'GPT-4'], var_name='Type', value_name='Score')
        df_en_melted = df_en.melt(id_vars=['Language'], value_vars=['human', 'GPT-4'], var_name='Type', value_name='Score')
        combined_df = pd.concat([df_gm_melted, df_en_melted], axis=0)

        # Determine whether to create a new figure
        if ax is None:
            fig, ax = plt.subplots(figsize=(8, 5))
            standalone = True
        else:
            standalone = False

        colors = sns.color_palette('Set3', 12)
        selected_colors = [colors[0], colors[11]]
        sns.boxplot(x='Language', y='Score', hue='Type', data=combined_df, palette=selected_colors, showfliers=False, ax=ax)
        ax.set_title(features_to_visualize_dict.get(feature, feature), fontsize=20)
        # set language as x-axis label
        ax.set_xlabel('')
        ax.set_ylabel('')
        if i == 0:
            ax.legend(title='', loc='lower left', fontsize=14)
        else:
            ax.get_legend().remove()

        # remove x-tick labels and ticks for top row
        if i < 5:
            ax.set_xlabel('')
            ax.tick_params(axis='x', labelsize=0, length=0)
        else:
            ax.set_xlabel('')
            ax.tick_params(axis='x', labelsize=16, length=6)
        plt.tight_layout()

        if standalone:
            plt.show()

    except Exception as e:
        print(f"Error processing feature {feature}: {e}")

def main(features, save_to_pdf=False):
    if save_to_pdf:
        pdf_new_page = PdfPages(f"../../viz/{GENERATION}_lang_diffs.pdf")
        fig = plt.figure(figsize=(20, 8))  # Adjusted for better visualization of two rows
        gs = gridspec.GridSpec(2, 5)  # 2 rows, 5 columns

        for i, feature in enumerate(features):
            ax = fig.add_subplot(gs[i // 5, i % 5])
            plot_feature(feature, i, ax)
        plt.tight_layout()
        plt.show()
        # pdf_new_page.savefig(fig)
        # pdf_new_page.close()
        plt.close(fig)
    else:
        for feature in features:
            plot_feature(feature, 0)


diff_features = ['pos_prop_DET', 'pos_prop_CCONJ',  'sentence_length_std', 'token_length_mean', 'sentence_length_mean', "entropy", "proportion_unique_tokens", "lix", "pos_prop_VERB", "type_token_ratio"]

# if want to viz all features across personas, use this
# viz_persona_features()

# if want to viz differences between languages, use this
main(diff_features, save_to_pdf=True)

# if want to vizualize each feature separately
# main(diff_features)


    











