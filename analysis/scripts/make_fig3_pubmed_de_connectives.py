import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# ##############################################################################
# # create a csv file with the differences between the usage of capitalized
# # connectives in the human and the gpt-3 texts for the top 30 connectives
# # produces Figure 1
# ##############################################################################

# Read the data from the CSV file into a DataFrame
df = pd.read_csv("../../feature_extraction/results/connectives/connectives_all_pubmed_de.csv")

# Sort the DataFrame based on the 'human_upper' column in ascending order and select the top 30 rows
df_sorted = df.sort_values(by='human_upper', ascending=False)

print(df_sorted)

# Calculate absolute differences
df_sorted['HU-CO'] = df_sorted['human_upper'] - df_sorted['continue_upper']
df_sorted['HU-EX'] = df_sorted['human_upper'] - df_sorted['explain_upper']
df_sorted['HU-CR'] = df_sorted['human_upper'] - df_sorted['create_upper']
df_sorted['CO-EX'] = df_sorted['continue_upper'] - df_sorted['explain_upper']
df_sorted['CO-CR'] = df_sorted['continue_upper'] - df_sorted['create_upper']
df_sorted['EX-CR'] = df_sorted['explain_upper'] - df_sorted['create_upper']

# Select only the required columns
df_final = df_sorted[['connective', 'human_upper', 'HU-CO', 'HU-EX', 'HU-CR', 'CO-EX', 'CO-CR', 'EX-CR']]

# write the data to a new CSV file
df_final.to_csv("../results/connectives_upper_pubmed_de_diffs.csv", index=False)

# ##############################################################################
# # make a heatmap
# ##############################################################################

sns.set_theme(style="white")

# use the first 25 rows
data = df_final.iloc[:30]

# make heat map for the values in the columns hu-co, hu-ex, hu-cr

data = data.set_index('connective')

# set the size of the plot
plt.figure(figsize=(5, 10))

# create a heatmap
ax = sns.heatmap(data=data[['HU-CO', 'HU-EX', 'HU-CR']], annot=True, fmt="d", linewidths=.5, cbar=False, cmap="YlGnBu")

# set the font size of the x and y axis labels
plt.yticks(fontsize=15)
plt.xticks(fontsize=15)


# place the x axis labels on the top
ax.xaxis.tick_top()

# set font size for the labels
ax.tick_params(labelsize=15) 

# set the color palette to set3
sns.set_palette("Set3")

# remove the y axis label
plt.ylabel("")

# save the plot as a pdf file
plt.savefig("../../viz/for_paper/connectives_cap_pubmed_de_heatmap.pdf", bbox_inches='tight')

# show the plot
plt.show()
plt.close()


