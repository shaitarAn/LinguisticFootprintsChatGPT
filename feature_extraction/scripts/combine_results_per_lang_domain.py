import pandas as pd
import os
import matplotlib.pyplot as plt
from features_list import features_to_visualize_dict

# initialize a dictionary with feature names as keys and empty lists as values
german_dict = {}
english_dict = {}

# create domain specific dictionaries
news_dict = {"english": {}, "german": {}}
science_dict = {"english": {}, "german": {}}
clinical_dict = {"english": {}, "german": {}}

german_corpora = ["pubmed_de", "zora_de", "20min", "cs_de", "ggponc"]
science_corpoa = ["pubmed_en", "pubmed_de", "zora_en", "zora_de"]
news_corpora = ["cnn", "20min", "cs_en", "cs_de"]
clinical_corpora = ["e3c", "ggponc"]

for corpus in ["pubmed_en", "pubmed_de", "zora_en", "zora_de", "cnn", "20min", "cs_en", "cs_de", "e3c", "ggponc"]:

    print("*" * 50)
    print(corpus)
    print("*" * 50)

    # Directory where the CSV files are located
    csv_directory = f"../results/per_corpus/{corpus}"  # Change this to the directory containing your CSV files

    # create list of features based on the first column of the first csv file
    first_csv = os.listdir(csv_directory)[0]
    dff = pd.read_csv(os.path.join(csv_directory, first_csv))
    corpus_features = dff.iloc[:, 0].tolist()

    features_to_extract = [f for f in features_to_visualize_dict.keys() if f in corpus_features]

    for feature_to_extract in features_to_extract:
        print(feature_to_extract)

        try:

            # print(feature_to_extract)
            combined_dataframe = []

            # Iterate through files in the directory
            for file_name in os.listdir(csv_directory):

                # Read the CSV file into a DataFrame
                df = pd.read_csv(os.path.join(csv_directory, file_name))

                # extract the feature data from the DataFrame
                feature_data = df.loc[df.iloc[:, 0] == feature_to_extract, :]

                # add feauture_data to combined_dataframe
                combined_dataframe.append(feature_data)

            # concatenate the dataframes
            combined_dataframe = pd.concat(combined_dataframe)

            # drop the first column
            combined_dataframe.drop(combined_dataframe.columns[0], axis=1, inplace=True)

            # reorder the columns so that they are in the following order: human, continue, explain, create
            combined_dataframe = combined_dataframe[["human", "continue", "explain", "create"]]

            # if corpus is german, add the dataframe to the german dataframe for the current feature
            if corpus in german_corpora:
                if feature_to_extract not in german_dict:
                    german_dict[feature_to_extract] = [combined_dataframe]
                else:
                    german_dict[feature_to_extract].append(combined_dataframe)
                if corpus in news_corpora:
                    if feature_to_extract not in news_dict["german"]:
                        news_dict["german"][feature_to_extract] = [combined_dataframe]
                    else:
                        news_dict["german"][feature_to_extract].append(combined_dataframe)
                elif corpus in science_corpoa:
                    if feature_to_extract not in science_dict["german"]:
                        science_dict["german"][feature_to_extract] = [combined_dataframe]
                    else:
                        science_dict["german"][feature_to_extract].append(combined_dataframe)
                elif corpus in clinical_corpora:
                    if feature_to_extract not in clinical_dict["german"]:
                        clinical_dict["german"][feature_to_extract] = [combined_dataframe]
                    else:
                        clinical_dict["german"][feature_to_extract].append(combined_dataframe)                       
            
            else:
                if feature_to_extract not in english_dict:
                    english_dict[feature_to_extract] = [combined_dataframe]
                else:
                    english_dict[feature_to_extract].append(combined_dataframe)
                if corpus in news_corpora:
                    if feature_to_extract not in news_dict["english"]:
                        news_dict["english"][feature_to_extract] = [combined_dataframe]
                    else:
                        news_dict["english"][feature_to_extract].append(combined_dataframe)
                elif corpus in science_corpoa:
                    if feature_to_extract not in science_dict["english"]:
                        science_dict["english"][feature_to_extract] = [combined_dataframe]
                    else:
                        science_dict["english"][feature_to_extract].append(combined_dataframe)
                elif corpus in clinical_corpora:
                    if feature_to_extract not in clinical_dict["english"]:
                        clinical_dict["english"][feature_to_extract] = [combined_dataframe]
                    else:
                        clinical_dict["english"][feature_to_extract].append(combined_dataframe)

            if not os.path.exists(f"../results/per_feature/{feature_to_extract}"):
                os.makedirs(f"../results/per_feature/{feature_to_extract}")

            # write the dataframe to a csv file
            combined_dataframe.to_csv(f"../results/per_feature/{feature_to_extract}/{corpus}.csv", index=False)

        except:
            print(f"Error in feature: {feature_to_extract}")
            continue


# iterate through the dictionaries and concatenate the dataframes
for feature, dataframes in german_dict.items():
    german_dict[feature] = pd.concat(dataframes)
    # print(german_dict[feature].head())
    # print(german_dict[feature].shape)
    if not os.path.exists(f"../results/per_language/german"):
        os.makedirs(f"../results/per_language/german")
    # write the dataframe to a csv file
    german_dict[feature].to_csv(f"../results/per_language/german/{feature}.csv", index=False)

for feature, dataframes in english_dict.items():
    english_dict[feature] = pd.concat(dataframes)
    print(english_dict[feature].head())
    # print(english_dict[feature].shape)
    if not os.path.exists(f"../results/per_language/english"):
        os.makedirs(f"../results/per_language/english")
    english_dict[feature].to_csv(f"../results/per_language/english/{feature}.csv", index=False)


# iterate through the dictionaries and concatenate the dataframes
for feature, dataframes in news_dict["german"].items():
    news_dict["german"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/news/german"):
        os.makedirs(f"../results/per_domain/news/german")
    news_dict["german"][feature].to_csv(f"../results/per_domain/news/german/{feature}.csv", index=False)

for feature, dataframes in news_dict["english"].items():
    news_dict["english"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/news/english"):
        os.makedirs(f"../results/per_domain/news/english")
    news_dict["english"][feature].to_csv(f"../results/per_domain/news/english/{feature}.csv", index=False)

for feature, dataframes in science_dict["german"].items():
    science_dict["german"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/science/german"):
        os.makedirs(f"../results/per_domain/science/german")
    science_dict["german"][feature].to_csv(f"../results/per_domain/science/german/{feature}.csv", index=False)

for feature, dataframes in science_dict["english"].items():
    science_dict["english"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/science/english"):
        os.makedirs(f"../results/per_domain/science/english")
    science_dict["english"][feature].to_csv(f"../results/per_domain/science/english/{feature}.csv", index=False)

for feature, dataframes in clinical_dict["german"].items():
    clinical_dict["german"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/clinical/german"):
        os.makedirs(f"../results/per_domain/clinical/german")
    clinical_dict["german"][feature].to_csv(f"../results/per_domain/clinical/german/{feature}.csv", index=False)

for feature, dataframes in clinical_dict["english"].items():
    clinical_dict["english"][feature] = pd.concat(dataframes)
    if not os.path.exists(f"../results/per_domain/clinical/english"):
        os.makedirs(f"../results/per_domain/clinical/english")
    clinical_dict["english"][feature].to_csv(f"../results/per_domain/clinical/english/{feature}.csv", index=False)

    
    
    
