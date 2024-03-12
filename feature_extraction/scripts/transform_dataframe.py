import pandas as pd
import csv
import os
import argparse

# make list of arguments
parser = argparse.ArgumentParser()
parser.add_argument("--features", "-f", type=str, required=True, help="type of feature to convert")
args = parser.parse_args()

type_of_feature = args.features

german_corpus = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]
english_corpus = ["pubmed_en", "zora_en", "cnn", "20min", "cs_en", "e3c"]

def transform_data(df, feature):

    df_pivot = df.pivot(index='file', columns='system', values=[feature])

    # Flatten the MultiIndex columns
    df_pivot.columns = [f'{col[1]}_{col[0]}' for col in df_pivot.columns]

    # Reset the index to convert 'file' back to a column
    df_pivot.reset_index(inplace=True)

    # reorder the columns so that they are in the following order: human_shannon, continue_shannon, explain_shannon, create_shannon
    df_pivot = df_pivot[["file", f"human_{feature}", f"continue_{feature}", f"create_{feature}", f"explain_{feature}"]]

    # rename columns to drop the '_shannon' suffix
    df_pivot.columns = ['file', 'human', 'continue', 'create', 'explain']
    # 
    # order the file column in ascending order
    df_pivot.sort_values(by='file', inplace=True)

    # remove the 'file' column
    df_pivot.drop(columns=['file'], inplace=True)

    return df_pivot
    

if type_of_feature == "morphology":

    # create empty list to collect all data per feature

    for feature in ['shannon', 'simpson']:

        language_data = []
        
        for corpus in german_corpus:

            df = pd.read_csv(f'../results/morphology/{corpus}.csv')

            # print(df.head())

            # mkdir results_shannon
            if feature == 'shannon':
                name = 'shannon_entropy'
                if not os.path.exists(f"../results/per_feature/{name}"):
                    os.makedirs(f"../results/per_feature/{name}")
                output_folder = f"../results/per_feature/{name}"
            else:
                name = 'simpson_diversity'
                if not os.path.exists(f"../results/per_feature/{name}"):
                    os.makedirs(f"../results/per_feature/{name}")
                output_folder = f"../results/per_feature/{name}"

            # Pivot the DataFrame to reshape it
            df_pivot = transform_data(df, feature)
            # print(df_pivot.head())

            df_pivot.to_csv(f"{output_folder}/{corpus}.csv", index=False)

            # add the feature data to the list
            language_data.append(df_pivot)
            # print("language_data", language_data)   
        
        # concatenate the dataframes in the list
        language_data = pd.concat(language_data)
        print(language_data)

        # create a folder for the language
        if not os.path.exists(f"../results/per_language/german"):
            os.makedirs(f"../results/per_language/german")

        language_data.to_csv(f"../results/per_language/german/{name}.csv", index=False)

elif type_of_feature == "lexical_richness":

    for feature in ['TTR', 'Yules', 'MTLD']:

        german_data = []
        english_data = []
        
        for corpus in german_corpus + english_corpus:

            df = pd.read_csv(f'../results/lexical_richness/{corpus}.csv')

            # mkdir results_shannon
            if feature == 'TTR':
                name = 'type_token_ratio'
                if not os.path.exists(f"../results/per_feature/{name}"):
                    os.makedirs(f"../results/per_feature/{name}")
                output_folder = f"../results/per_feature/{name}"
            elif feature == 'Yules':
                name = 'yules_k'
                if not os.path.exists(f"../results/per_feature/{name}"):
                    os.makedirs(f"../results/per_feature/{name}")
                output_folder = f"../results/per_feature/{name}"
            else:
                name = 'mtld'
                if not os.path.exists(f"../results/per_feature/{name}"):
                    os.makedirs(f"../results/per_feature/{name}")
                output_folder = f"../results/per_feature/{name}"

            # Pivot the DataFrame to reshape it
            df_pivot = transform_data(df, feature)

            # Write the resulting DataFrame to a CSV file
            df_pivot.to_csv(f"{output_folder}/{corpus}.csv", index=False)

            # add the feature data to the list
            if corpus in german_corpus:
                print(feature, corpus)
                german_data.append(df_pivot)
            else:
                english_data.append(df_pivot)
            
        # concatenate the dataframes in the list
        german_data = pd.concat(german_data)
        print(german_data)
        english_data = pd.concat(english_data)

        if not os.path.exists(f"../results/per_language/german"):
            os.makedirs(f"../results/per_language/german")
        german_data.to_csv(f"../results/per_language/german/{name}.csv", index=False)
        
        if not os.path.exists(f"../results/per_language/english"):
            os.makedirs(f"../results/per_language/english")
        english_data.to_csv(f"../results/per_language/english/{name}.csv", index=False)