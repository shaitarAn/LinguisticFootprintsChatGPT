import pandas as pd
import os
import matplotlib.pyplot as plt

features_to_visualize = pd.read_csv("../results/final/pubmed_en/14.csv", index_col=0).index.tolist()

print(features_to_visualize)
print(len(features_to_visualize))


# initialize a dictionary with feature names as keys and empty lists as values
german_dict = {feature: [] for feature in features_to_visualize}
english_dict = {feature: [] for feature in features_to_visualize}


for corpus in ["pubmed_en", "pubmed_de", "zora_en", "zora_de", "cnn", "20min", "cs_en", "cs_de", "e3c", "ggponc"]:

    # Directory where the CSV files are located
    csv_directory = f"../results/final/{corpus}"  # Change this to the directory containing your CSV files

    # features_to_visualize = ['n_stop_words', 'alpha_ratio', 'mean_word_length', 'doc_length', 'duplicate_ngram_chr_fraction_5', 'duplicate_ngram_chr_fraction_6', 'duplicate_ngram_chr_fraction_7', 'duplicate_ngram_chr_fraction_8', 'duplicate_ngram_chr_fraction_9', 'duplicate_ngram_chr_fraction_10', 'top_ngram_chr_fraction_2', 'top_ngram_chr_fraction_3', 'top_ngram_chr_fraction_4', 'oov_ratio', 'pos_prop_ADJ', 'pos_prop_NOUN', 'pos_prop_AUX', 'pos_prop_VERB', 'pos_prop_ADV', 'pos_prop_PUNCT', 'pos_prop_PRON', 'pos_prop_ADP', 'pos_prop_DET', 'pos_prop_CCONJ', 'pos_prop_PART', 'pos_prop_NUM', 'pos_prop_SYM', 'pos_prop_X', 'pos_prop_PROPN', 'pos_prop_SCONJ', 'pos_prop_INTJ', 'dependency_distance_mean', 'dependency_distance_std', 'prop_adjacent_dependency_relation_mean', 'prop_adjacent_dependency_relation_std', 'entropy', 'perplexity', 'per_word_perplexity', 'token_length_mean', 'token_length_median', 'token_length_std', 'sentence_length_mean', 'sentence_length_median', 'sentence_length_std', 'syllables_per_token_mean', 'syllables_per_token_median', 'syllables_per_token_std', 'n_tokens', 'n_unique_tokens', 'proportion_unique_tokens', 'n_characters', 'n_sentences', 'first_order_coherence', 'second_order_coherence', 'flesch_reading_ease', 'flesch_kincaid_grade', 'smog', 'gunning_fog', 'automated_readability_index', 'coleman_liau_index', 'lix', 'rix', 'connectives', 'connectives_cap', 'passed_quality_check', 'pos_prop_SPACE', 'proportion_bullet_points']

    for feature_to_extract in features_to_visualize:

        combined_dataframe = []

        # Iterate through files in the directory
        for file_name in os.listdir(csv_directory):

            # Read the CSV file into a DataFrame
            df = pd.read_csv(os.path.join(csv_directory, file_name))

            try:

                # extract the feature data from the DataFrame
                feature_data = df.loc[df.iloc[:, 0] == feature_to_extract, :]

                # add feauture_data to combined_dataframe
                combined_dataframe.append(feature_data)

            except IndexError:
                continue

        # concatenate the dataframes
        combined_dataframe = pd.concat(combined_dataframe)

        # drop the first column
        combined_dataframe.drop(combined_dataframe.columns[0], axis=1, inplace=True)

        print(corpus, feature_to_extract)
        # print(combined_dataframe.head())
        print(combined_dataframe.shape)

        # reorder teh columns so that they are in the following order: human, continue, explain, create
        combined_dataframe = combined_dataframe[["human", "continue", "explain", "create"]]

        # if corpus is german, add the dataframe to the german dataframe for the current feature
        if corpus in ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]:
            german_dict[feature_to_extract].append(combined_dataframe)
        else:
            english_dict[feature_to_extract].append(combined_dataframe)

        if not os.path.exists(f"../results/per_feature/{feature_to_extract}"):
            os.makedirs(f"../results/per_feature/{feature_to_extract}")

        # write the dataframe to a csv file
        if feature_to_extract == "flesch_reading_ease" and corpus in ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]:
            pass
        else:
            combined_dataframe.to_csv(f"../results/per_feature/{feature_to_extract}/{corpus}.csv", index=False)


# iterate through the dictionaries and concatenate the dataframes
for feature, dataframes in german_dict.items():
    german_dict[feature] = pd.concat(dataframes)
    # print(german_dict[feature].head())
    print(german_dict[feature].shape)
    if not os.path.exists(f"../results/per_language/german"):
        os.makedirs(f"../results/per_language/german")
    # write the dataframe to a csv file
    german_dict[feature].to_csv(f"../results/per_language/german/{feature}.csv", index=False)

for feature, dataframes in english_dict.items():
    english_dict[feature] = pd.concat(dataframes)
    # print(english_dict[feature].head())
    print(english_dict[feature].shape)
    if not os.path.exists(f"../results/per_language/english"):
        os.makedirs(f"../results/per_language/english")
    # write the dataframe to a csv file
    english_dict[feature].to_csv(f"../results/per_language/english/{feature}.csv", index=False)