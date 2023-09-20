import pandas as pd
import os
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")

args = parser.parse_args()
corpus = args.corpus

# Directory where the CSV files are located
csv_directory = "../results_truncated"  # Change this to the directory containing your CSV files

# Initialize an empty DataFrame to store the combined data
combined_dataframe = pd.DataFrame()

features_to_visualize = ['token_length_mean', 'token_length_median', 'token_length_std', 'sentence_length_mean', 'sentence_length_median', 'sentence_length_std', 'syllables_per_token_mean', 'syllables_per_token_median', 'syllables_per_token_std', 'n_tokens', 'n_unique_tokens', 'proportion_unique_tokens', 'n_characters', 'n_sentences', 'first_order_coherence', 'second_order_coherence', 'entropy', 'perplexity', 'per_word_perplexity', 'flesch_reading_ease', 'flesch_kincaid_grade', 'smog', 'gunning_fog', 'automated_readability_index', 'coleman_liau_index', 'lix', 'rix', 'pos_prop_VERB', 'pos_prop_DET', 'pos_prop_ADJ', 'pos_prop_PROPN', 'pos_prop_NOUN', 'pos_prop_ADV', 'pos_prop_PUNCT', 'pos_prop_NUM', 'pos_prop_SCONJ', 'pos_prop_PRON', 'pos_prop_AUX', 'pos_prop_PART', 'pos_prop_ADP', 'pos_prop_CCONJ', 'dependency_distance_mean', 'dependency_distance_std', 'prop_adjacent_dependency_relation_mean', 'prop_adjacent_dependency_relation_std', 'n_stop_words', 'alpha_ratio', 'mean_word_length', 'doc_length', 'duplicate_ngram_chr_fraction_5', 'duplicate_ngram_chr_fraction_6', 'top_ngram_chr_fraction_2', 'top_ngram_chr_fraction_3', 'top_ngram_chr_fraction_4', 'connectives', 'oov_ratio', 'duplicate_ngram_chr_fraction_7']

for feature_to_extract in features_to_visualize:

    combined_dataframe = pd.DataFrame()

    # List to store parameter names
    parameter_names = []

    # Iterate through files in the directory
    for file_name in os.listdir(csv_directory):
        # Check if the file matches the naming pattern for the current corpus
        if file_name.startswith(f"combined_{corpus}_"):

            # Extract the parameter name from the file name
            params = "_".join(file_name[:-4].split("_")[-2:])


            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join(csv_directory, file_name))

            # Set the first column as the index
            df.set_index(df.columns[0], inplace=True)

            feature_data = df.loc[feature_to_extract].to_frame()

            # Replace the column name "connectives" with the parameter value
            feature_data.columns = [params]

            # Store the parameter name
            parameter_names.append(params)
            
            # print(feature_data)

            # add feauture_data to combined_dataframe
            combined_dataframe = pd.concat([combined_dataframe, feature_data], axis=1)


    combined_dataframe = combined_dataframe.transpose()
    # print(combined_dataframe)

    # Convert all columns in the DataFrame to numeric
    combined_dataframe = combined_dataframe.apply(pd.to_numeric, errors='ignore')

    if not os.path.exists(f"../plots/{feature_to_extract}"):
        os.makedirs(f"../plots/{feature_to_extract}")

    # Check if all columns are numeric
    if combined_dataframe.select_dtypes(include='number').empty:
        print("No numeric data to plot.")
    else:
        # Create a bar plot and save it as a PNG file
        # x-axis should be values from the dataframe
        # y-axis should be the parameter names
        # title should be the name of the corpus
        combined_dataframe.plot.barh(title=corpus+" "+feature_to_extract)
        # add a name for the y-axis
        plt.ylabel("temperature, frequency penalty")
        plt.savefig(f"../plots/{feature_to_extract}/{corpus}.png", bbox_inches='tight')
        plt.close()


