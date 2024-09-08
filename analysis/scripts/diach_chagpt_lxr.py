import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

path_to_data = "../../feature_extraction/"
corpus = "20min"
metrics = "lexical_richness" # or "morphology"

# Step 1: Load the two CSV files into DataFrames
file1_path = os.path.join(path_to_data, "2309/results", metrics, f"{corpus}.csv")
file2_path = os.path.join(path_to_data, "2403/results", metrics, f"{corpus}.csv")
file3_path = os.path.join(path_to_data, "2407/results", metrics, f"{corpus}.csv")

df1 = pd.read_csv(file1_path)
df2 = pd.read_csv(file2_path)
df3 = pd.read_csv(file3_path)

# Step 2: Add a 'dataset' column to differentiate between the two datasets
df1['dataset'] = 'GPT3 09.23'
df2['dataset'] = 'GPT4 03.24'
df3['dataset'] = 'GPT4o 07.24'

# Step 3: Combine the DataFrames
combined_df = pd.concat([df1, df2, df3])

# Step 4: Visualize the data using Seaborn and Matplotlib

# Set the plotting style
sns.set(style="whitegrid")

if metrics == "lexical_richness":
    # Plot for TTR
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='system', y='TTR', hue='dataset', data=combined_df)
    plt.title(f'Type-Token Ratio (TTR) Across Different in {corpus}')
    plt.xlabel('System')
    plt.ylabel('TTR')
    plt.legend(title='Generation')
    plt.tight_layout()
    plt.show()

    # Plot for Yules
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='system', y='Yules', hue='dataset', data=combined_df)
    plt.title(f'Yules Measure Across Different in {corpus}')
    plt.xlabel('System')
    plt.ylabel('Yules Measure')
    plt.legend(title='Generation')
    plt.tight_layout()
    plt.show()

    # Plot for MTLD
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='system', y='MTLD', hue='dataset', data=combined_df)
    plt.title(f'Measure of Textual Lexical Diversity (MTLD) in {corpus}')
    plt.xlabel('System')
    plt.ylabel('MTLD')
    plt.legend(title='Generation')
    plt.tight_layout()
    plt.show()

elif metrics == "morphology":

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='system', y='shannon', hue='dataset', data=combined_df)
    plt.title(f'Shannon Entropy Across Different in {corpus}')
    plt.xlabel('System')
    plt.ylabel('Shannon')
    plt.legend(title='Generation')
    plt.tight_layout()
    plt.show()

    # Plot for Yules
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='system', y='simpson', hue='dataset', data=combined_df)
    plt.title(f'Simpson Diversity Across Different in {corpus}')
    plt.xlabel('System')
    plt.ylabel('Simpson Diversity')
    plt.legend(title='Generation')
    plt.tight_layout()
    plt.show()