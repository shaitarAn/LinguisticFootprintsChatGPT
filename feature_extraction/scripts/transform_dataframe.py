import pandas as pd
import csv
import os
import argparse
# from config import GERMAN_CORPORA, ENGLISH_CORPORA, SCIENCE_CORPORA, NEWS_CORPORA, CLINICAL_CORPORA
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)


# make list of arguments
parser = argparse.ArgumentParser()
parser.add_argument("--feature", "-f", type=str, required=True, help="type of feature to convert")
parser.add_argument('-o', '--output_dir', type=str, required=True, help="Directory where all results and outputs will go.")
parser.add_argument("-c", "--config", type=str, required=True, help="Path to YAML configuration file.")
args = parser.parse_args()

type_of_feature = args.feature

config = load_config(args.config)
GERMAN_CORPORA = config['corpora']['german']
ENGLISH_CORPORA = config['corpora']['english']

# create domain specific dictionaries
news_dict = {"english": {}, "german": {}}
science_dict = {"english": {}, "german": {}}
clinical_dict = {"english": {}, "german": {}}

def transform_data(df, feature):

    df_pivot = df.pivot(index='file', columns='system', values=[feature])

    # Flatten the MultiIndex columns
    df_pivot.columns = [f'{col[1]}_{col[0]}' for col in df_pivot.columns]

    # Reset the index to convert 'file' back to a column
    df_pivot.reset_index(inplace=True)

    # reorder the columns so that they are in the following order: human_shannon, continue_shannon, explain_shannon, create_shannon
    # df_pivot = df_pivot[["file", f"human_{feature}", f"continue_{feature}", f"create_{feature}", f"explain_{feature}"]]

    # rename columns to drop the '_shannon' suffix
    df_pivot.columns = df_pivot.columns.str.replace(f'_{feature}', '')
    
    # order the file column in ascending order
    df_pivot.sort_values(by='file', inplace=True)

    # remove the 'file' column
    df_pivot.drop(columns=['file'], inplace=True)

    return df_pivot
    

if type_of_feature == "morphology":

    # create empty list to collect all data per feature
    for feature in ['shannon', 'simpson']:

        language_data = []
        
        for corpus in GERMAN_CORPORA:

            df = pd.read_csv(f"{args.output_dir}/morphology/{corpus}.csv")

            # print(df.head())

            # mkdir results_shannon
            if feature == 'shannon':
                name = 'shannon_entropy'
                if not os.path.exists(f"{args.output_dir}/per_feature/{name}"):
                    os.makedirs(f"{args.output_dir}/per_feature/{name}")
                output_folder = f"{args.output_dir}/per_feature/{name}"

            else:
                name = 'simpson_diversity'
                if not os.path.exists(f"{args.output_dir}/per_feature/{name}"):
                    os.makedirs(f"{args.output_dir}/per_feature/{name}")
                output_folder = f"{args.output_dir}/per_feature/{name}"

            # Pivot the DataFrame to reshape it
            df_pivot = transform_data(df, feature)

            df_pivot.to_csv(f"{output_folder}/{corpus}.csv", index=False)

            # add the feature data to the list
            language_data.append(df_pivot)
            # print("language_data", language_data)   

            if corpus in NEWS_CORPORA:
                # print(corpus, feature)
                # print(df_pivot.head())
                if feature not in news_dict["german"]:
                    # print("feature", feature)
                    news_dict["german"][feature] = [df_pivot]
                else:
                    news_dict["german"][feature].append(df_pivot)
            elif corpus in SCIENCE_CORPORA:
                if feature not in science_dict["german"]:
                    science_dict["german"][feature] = [df_pivot]
                else:
                    science_dict["german"][feature].append(df_pivot)
            elif corpus in CLINICAL_CORPORA:
                if feature not in clinical_dict["german"]:
                    clinical_dict["german"][feature] = [df_pivot]
                else:
                    clinical_dict["german"][feature].append(df_pivot)      
        
        # concatenate the dataframes in the list
        language_data = pd.concat(language_data)
        # print(language_data)

        # create a folder for the language
        if not os.path.exists(f"{args.output_dir}/per_language/german"):
            os.makedirs(f"{args.output_dir}/per_language/german")

        language_data.to_csv(f"{args.output_dir}/per_language/german/{name}.csv", index=False)

elif type_of_feature == "lexical_richness":

    for feature in ['TTR', 'Yules', 'MTLD']:

        german_data = []
        english_data = []
        
        for corpus in GERMAN_CORPORA + ENGLISH_CORPORA:

            df = pd.read_csv(f'{args.output_dir}/lexical_richness/{corpus}.csv')

            # mkdir results_shannon
            if feature == 'TTR':
                name = 'type_token_ratio'
                if not os.path.exists(f"{args.output_dir}/per_feature/{name}"):
                    os.makedirs(f"{args.output_dir}/per_feature/{name}")
                output_folder = f"{args.output_dir}/per_feature/{name}"
            elif feature == 'Yules':
                name = 'yules_k'
                if not os.path.exists(f"{args.output_dir}/per_feature/{name}"):
                    os.makedirs(f"{args.output_dir}/per_feature/{name}")
                output_folder = f"{args.output_dir}/per_feature/{name}"
            else:
                name = 'mtld'
                if not os.path.exists(f"{args.output_dir}/per_feature/{name}"):
                    os.makedirs(f"{args.output_dir}/per_feature/{name}")
                output_folder = f"{args.output_dir}/per_feature/{name}"

            # Pivot the DataFrame to reshape it
            df_pivot = transform_data(df, feature)

            # Write the resulting DataFrame to a CSV file
            df_pivot.to_csv(f"{output_folder}/{corpus}.csv", index=False)

            # add the feature data to the list
            if corpus in GERMAN_CORPORA:
                # print(feature, corpus)
                german_data.append(df_pivot)

                if corpus in NEWS_CORPORA:
                    # print(corpus, feature)
                    # print(df_pivot.head())

                    if feature not in news_dict["german"]:
                        # print("feature", feature)
                        news_dict["german"][feature] = [df_pivot]
                    else:
                        news_dict["german"][feature].append(df_pivot)
                elif corpus in SCIENCE_CORPORA:
                    if feature not in science_dict["german"]:
                        science_dict["german"][feature] = [df_pivot]
                    else:
                        science_dict["german"][feature].append(df_pivot)
                elif corpus in CLINICAL_CORPORA:
                    if feature not in clinical_dict["german"]:
                        clinical_dict["german"][feature] = [df_pivot]
                    else:
                        clinical_dict["german"][feature].append(df_pivot)      
            else:
                english_data.append(df_pivot)
                if corpus in NEWS_CORPORA:
                # print(corpus, feature)
                # print(df_pivot.head())
                    if feature not in news_dict["english"]:
                        # print("feature", feature)
                        news_dict["english"][feature] = [df_pivot]
                    else:
                        news_dict["english"][feature].append(df_pivot)
                elif corpus in SCIENCE_CORPORA:
                    if feature not in science_dict["english"]:
                        science_dict["english"][feature] = [df_pivot]
                    else:
                        science_dict["english"][feature].append(df_pivot)
                elif corpus in CLINICAL_CORPORA:
                    if feature not in clinical_dict["english"]:
                        clinical_dict["english"][feature] = [df_pivot]
                    else:
                        clinical_dict["english"][feature].append(df_pivot)      
            
        # concatenate the dataframes in the list
        german_data = pd.concat(german_data)
        # print(german_data)
        english_data = pd.concat(english_data)

        if not os.path.exists(f"{args.output_dir}/per_language/german"):
            os.makedirs(f"{args.output_dir}/per_language/german")
        german_data.to_csv(f"{args.output_dir}/per_language/german/{name}.csv", index=False)
        
        if not os.path.exists(f"{args.output_dir}/per_language/english"):
            os.makedirs(f"{args.output_dir}/per_language/english")
        english_data.to_csv(f"{args.output_dir}/per_language/english/{name}.csv", index=False)


# iterate through the dictionaries and concatenate the dataframes
for feature, dataframes in news_dict["german"].items():
    # print("feature", feature)
    # print("dataframes", len(dataframes))
    news_dict["german"][feature] = pd.concat(dataframes)
    # print(news_dict["german"][feature].head())
    if not os.path.exists(f"{args.output_dir}/per_domain/news/german"):
        os.makedirs(f"{args.output_dir}/per_domain/news/german")
    news_dict["german"][feature].to_csv(f"{args.output_dir}/per_domain/news/german/{feature}.csv", index=False)
    print(news_dict["german"][feature].head())

for feature, dataframes in news_dict["english"].items():
    print("feature", feature)
    print("dataframes", len(dataframes))
    news_dict["english"][feature] = pd.concat(dataframes)
    print(news_dict["english"][feature].head())
    if not os.path.exists(f"{args.output_dir}/per_domain/news/english"):
        os.makedirs(f"{args.output_dir}/per_domain/news/english")
    news_dict["english"][feature].to_csv(f"{args.output_dir}/per_domain/news/english/{feature}.csv", index=False)

for feature, dataframes in science_dict["german"].items():
    science_dict["german"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"{args.output_dir}/per_domain/science/german"):
        os.makedirs(f"{args.output_dir}/per_domain/science/german")
    science_dict["german"][feature].to_csv(f"{args.output_dir}/per_domain/science/german/{feature}.csv", index=False)

for feature, dataframes in science_dict["english"].items():
    science_dict["english"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"{args.output_dir}/per_domain/science/english"):
        os.makedirs(f"{args.output_dir}/per_domain/science/english")
    science_dict["english"][feature].to_csv(f"{args.output_dir}/per_domain/science/english/{feature}.csv", index=False)

for feature, dataframes in clinical_dict["german"].items():
    clinical_dict["german"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"{args.output_dir}/per_domain/clinical/german"):
        os.makedirs(f"{args.output_dir}/per_domain/clinical/german")
    clinical_dict["german"][feature].to_csv(f"{args.output_dir}/per_domain/clinical/german/{feature}.csv", index=False)

for feature, dataframes in clinical_dict["english"].items():
    clinical_dict["english"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"{args.output_dir}/per_domain/clinical/english"):
        os.makedirs(f"{args.output_dir}/per_domain/clinical/english")
    clinical_dict["english"][feature].to_csv(f"{args.output_dir}/per_domain/clinical/english/{feature}.csv", index=False)

