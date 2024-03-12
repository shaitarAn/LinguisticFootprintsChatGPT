import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import json

input_json_en = '../results/english_significant_features_0.01.json'
input_json_de = '../results/german_significant_features_0.01.json'

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
    for method, features in f.items():
        if method == 'bon':  # Considering 'bon' method
            for feature in features:
                if feature not in feature_persona_mapping:
                    feature_persona_mapping[feature] = {}
                feature_persona_mapping[feature][persona] = 1

# iterate over persona and features in German data
# if the feature is already in the dictionary, if the persona is already in the dictionary, increment the count
for persona, f in significant_features_de.items():
    for method, features in f.items():
        if method == 'bon':  # Considering 'bon' method
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
