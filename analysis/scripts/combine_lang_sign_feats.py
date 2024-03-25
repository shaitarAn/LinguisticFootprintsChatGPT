import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json
import argparse

# parse the input arguments
parser = argparse.ArgumentParser(description='Combine the significant features from the English and German data')
parser.add_argument('--alpha', '-a', type=float, default=0.01, help='the significance level (default: 0.01)')
# add method argument
parser.add_argument('--method', '-m', choices=['bh', 'holm', 'bon'], default='bh', help='the method for multiple hypothesis testing correction (default: Benjamini-Hochberg)')

args = parser.parse_args()
alpha = args.alpha
method = args.method

input_json_en = f'../results/english_significant_features_{alpha}.json'
input_json_de = f'../results/german_significant_features_{alpha}.json'

# extract data from the json file
significant_features_en = {}
with open(input_json_en, 'r') as f:
    significant_features_en = json.load(f)

# extract data from the json file
significant_features_de = {}
with open(input_json_de, 'r') as f:
    significant_features_de = json.load(f)

personas_dict = {'human-continue': 'Hu-Co', 'human-explain': 'Hu-Ex', 'human-create': 'Hu-Cr', 'continue-explain': 'Co-Ex', 'continue-create': 'Co-Cr', 'explain-create': 'Ex-Cr'}

# Initialize a dictionary to store feature-persona mapping
feature_persona_mapping = {}

# iterate over persona and features in the English and German data
for persona, f in significant_features_en.items():
    for m, features in f.items():
        if m == method:  # Considering 'bon' method
            for feature in features:
                if feature not in feature_persona_mapping:
                    feature_persona_mapping[feature] = {}
                feature_persona_mapping[feature][persona] = 1

# iterate over persona and features in German data
# if the feature is already in the dictionary, if the persona is already in the dictionary, increment the count
for persona, f in significant_features_de.items():
    for m, features in f.items():
        if m == method:  # Considering 'bon' method
            for feature in features:
                if feature not in feature_persona_mapping:
                    feature_persona_mapping[feature] = {}
                if persona in feature_persona_mapping[feature]:
                    feature_persona_mapping[feature][persona] += 1
                else:
                    feature_persona_mapping[feature][persona] = 3

# Convert the feature-persona mapping dictionary to a DataFrame
df = pd.DataFrame.from_dict(feature_persona_mapping, orient='index')
df.fillna(0, inplace=True)  # Replace NaN with 0 for features not significant for a persona

# Sort the DataFrame by features in alphabetical order
df = df.sort_index()

# Rename the columns to the persona abbreviations
df.columns = [personas_dict[p] for p in df.columns]

# Save the DataFrame to a CSV file
output_csv = '../results/significant_features_table.csv'
df.to_csv(output_csv)
