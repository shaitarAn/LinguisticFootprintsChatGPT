import pandas as pd
from scipy import stats
from scipy.stats import ttest_ind
import itertools


# check significane of the differences between the means of one feature for combined english and german corpora
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
from itertools import combinations
from viz_helper import plot_means, plot_distribtuions

# Load the data
f = "shannon_entropy"
# feature = f"../../feature_extraction/results/per_language/english/{f}.csv"
# feature_other_lang = f"../../feature_extraction/results/per_language/german/{f}.csv"
feature_other_lang = f"../../feature_extraction/results/per_feature/shannon_entropy/20min.csv"

# dfe = pd.read_csv(feature)
dfg = pd.read_csv(feature_other_lang)

# Combine the dataframes
# df = pd.concat([dfe, dfg])
df = dfg
# write the data to a new CSV file
df.to_csv(f"test_full_{f}.csv", index=False)

# make a boxplot
sns.set_theme(style="whitegrid")
plt.figure(figsize=(8, 8))
ax = sns.boxplot(data=df, palette="Set3")
plt.show()


# print size of the dataframe
# print(dfe.shape)
print(dfg.shape)
print(df.shape)

# Check significance of the differences between the means of the different personas
personas = ['human', 'continue', 'explain', 'create']

# Initialize a matrix to store p-values
p_value_matrix = pd.DataFrame(index=personas, columns=personas)

for p1, p2 in combinations(personas, 2):
    # Check if both samples have a normal distribution
    if stats.shapiro(df[p1])[1] < 0.05 and stats.shapiro(df[p2])[1] < 0.05:
        # Use the Mann-Whitney U test
        statistic, pvalue = stats.mannwhitneyu(df[p1], df[p2], alternative='two-sided')
        print(p1, p2, pvalue)
        if pvalue > 0.05:
            print(p1, p2, "Not significant")

    else:
        # Use the t-test
        statistic, pvalue = stats.ttest_ind(df[p1], df[p2])
        print(p1, p2, pvalue)
        if pvalue > 0.05:
            print(p1, p2, "Not significant")
    
    # Store the p-value in the matrix
    p_value_matrix.loc[p1, p2] = pvalue
    p_value_matrix.loc[p2, p1] = pvalue

print("p_value_matrix")
print(p_value_matrix)

# # Convert p-values to a heatmap-friendly format
# p_value_matrix = p_value_matrix.astype(float)

# # Set the size of the plot
# plt.figure(figsize=(8, 8))

# # Create a heatmap of the p-values
# ax = sns.heatmap(p_value_matrix, annot=True, fmt=".3f", linewidths=.5, cbar=False, cmap="YlGnBu", annot_kws={"size": 20})

# # Display the plot
# plt.show()
# ##############################################################################
