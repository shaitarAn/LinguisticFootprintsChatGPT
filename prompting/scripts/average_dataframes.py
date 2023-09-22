import os
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")
parser.add_argument("--params", type=str, required=True, help="combined params to use in file naming")

args = parser.parse_args()

corpus = args.corpus
params = args.params

folder_path = f"../results_truncated/{corpus}/"  # Update with the path to your folder
files = os.listdir(folder_path)

# for corpus in ["cnn", "e3c", "pubmed_en", "pubmed_de", "ggponc", "20min"]:

new_frames = []


# Initialize a list to store DataFrames
dataframes = []

# Process each CSV file and determine common columns
common_columns = None

for file in files:
    if file.startswith(file) and params in file:
        # print(file)
        df = pd.read_csv(os.path.join(folder_path, file))
        # print(df)
        # print("-------------------------")
        if common_columns is None:
            common_columns = df.columns.tolist()
        else:
            common_columns = list(set(common_columns).intersection(df.columns.tolist()))

        dataframes.append(df)

if common_columns:
    # Re-order columns consistently based on the common columns
    for i in range(len(dataframes)):
        df = dataframes[i]
        df = df[common_columns]
        # print(df)
        # rename the column "unnamed: 0" to "feature"
        df = df.rename(columns={"Unnamed: 0": "feature"})
        # drop the row where the value in the first column is "passed_quality_check"
        df = df[df['feature'] != "passed_quality_check"] 
        # turn the feature column into the index
        df.set_index('feature', inplace=True) 
        df = df.astype(float)
        # print(df)
        # print value for row "connectives"
        # print(df.loc['connectives'])
        # print(df.columns)
        new_frames.append(df)
        # dataframes[i] = df

    # print("--------------------------------------------------")


    # calculate mean for each row and column in the dataframes
   
average_human = pd.concat((new_frames)).groupby("feature", as_index=True, sort=False)['human'].mean()
average_continue = pd.concat((new_frames)).groupby("feature", as_index=True, sort=False)['continue'].mean()
average_explain = pd.concat((new_frames)).groupby("feature", as_index=True, sort=False)['explain'].mean()
average_create = pd.concat((new_frames)).groupby("feature", as_index=True, sort=False)['create'].mean()

df = pd.concat([average_human, average_create, average_continue, average_explain], axis=1)

# print(df.loc['connectives'])
# write the dataframe to a csv file
df.to_csv(f"../results_truncated/combined_{corpus}_{params}.csv")

# print the first column of the dataframe as a list
# print(df.index.tolist())






