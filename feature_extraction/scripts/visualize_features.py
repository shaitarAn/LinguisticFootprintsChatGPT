import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def visualize_files(output_directory, images_directory, excluded_features, feature_groups):
    if not os.path.exists(images_directory):
        os.makedirs(images_directory)
    
    for group_name, group_features in feature_groups.items():
        pdf_filename = f"{images_directory}/{group_name}_{corpus}.pdf"
    
        # Create a PDF file
        with PdfPages(pdf_filename) as pdf:
            for file_name in os.listdir(output_directory):
                if file_name.endswith(".csv"):
                    feature_name = file_name.split('.')[0]
                    
                    # Skip excluded features
                    if feature_name in excluded_features:
                        continue

                    # Skip features not in the current group
                    if feature_name not in group_features:
                        continue

                    file_path = os.path.join(output_directory, file_name)
                    df = pd.read_csv(file_path)

                    plt.figure(figsize=(10, 5))
                    plt.plot(df['gpt'], label="gpt")
                    plt.plot(df['human'], label="human")
                    plt.title(feature_name)
                    plt.xlabel("Document")
                    plt.ylabel("Value")
                    plt.legend()

                    # Save the figure as a PNG file
                    image_file_name = f"{file_name.replace('.csv', '')}.png"
                    image_file_path = os.path.join(images_directory, image_file_name)
                    plt.savefig(image_file_path)

                    # Add the figure to the PDF file
                    pdf.savefig(plt.gcf())
                    plt.close()

feature_groups = {
    "readability": ['flesch_reading_ease', 'flesch_kincaid_grade', 'gunning_fog', 'automated_readability_index', 'coleman_liau_index', 'lix', 'rix', "syllables_per_token_median"],
    
    "dep_distance": ['dependency_distance_mean', 'dependency_distance_std',
    'prop_adjacent_dependency_relation_mean', 'prop_adjacent_dependency_relation_std'],
    
    "quality": ['passed_quality_check', "n_stop_words", 'alpha_ratio', 'mean_word_length', 'doc_length', 'symbol_to_word_ratio_#', 'proportion_ellipsis', 'proportion_bullet_points', 'contains_lorem ipsum', 'duplicate_line_chr_fraction', 'duplicate_paragraph_chr_fraction','duplicate_ngram_chr_fraction_5', 'duplicate_ngram_chr_fraction_6', 'duplicate_ngram_chr_fraction_7', 'duplicate_ngram_chr_fraction_8', 'duplicate_ngram_chr_fraction_9', 'duplicate_ngram_chr_fraction_10', 'top_ngram_chr_fraction_2','top_ngram_chr_fraction_3', 'top_ngram_chr_fraction_4', 'oov_ratio'],
    
    "descriptive_stats": ['token_length_mean', 'token_length_median', 'token_length_std', 'sentence_length_mean', 'sentence_length_median', 'sentence_length_std', 'syllables_per_token_mean', 'syllables_per_token_median', 'syllables_per_token_std', 'n_tokens', 'n_unique_tokens', 'proportion_unique_tokens', 'n_characters', 'n_sentences'],
    
    "information_theory": ["entropy", "perplexity", "per_word_perplexity"],

    "pos_distributions": ["pos_prop_ADJ", "pos_prop_ADP", "pos_prop_ADV", "pos_prop_AUX", "pos_prop_CCONJ", "pos_prop_DET", "pos_prop_NOUN", "pos_prop_NUM", "pos_prop_PART", "pos_prop_PRON", "pos_prop_PROPN", "pos_prop_PUNCT", "pos_prop_SCONJ", "pos_prop_VERB"],

    "coherence":  ["first_order_coherence", "second_order_coherence"]
}

for corpus in ["20min", "cnn", "e3c", "GGPONC", "pubmed_de", "pubmed_en", "zora_de", "zora_en"]:
    
    output_directory = f"../output/paired_features_{corpus}"
    images_directory = f"../results/feature_visualizations_{corpus}"
    excluded_features = ["contains_lorem ipsum", "proportion_ellipsis", "symbol_to_word_ratio_#", "file_id", "proportion_bullet_points", "text", "duplicate_paragraph_chr_fraction", "duplicate_line_chr_fraction"]

    visualize_files(output_directory, images_directory, excluded_features, feature_groups)
