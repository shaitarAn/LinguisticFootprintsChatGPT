import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

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

# Calculate absolute differences human values are at zero
# df_sorted['HU-CO'] = df_sorted['human_upper'] - df_sorted['continue_upper']
# df_sorted['HU-EX'] = df_sorted['human_upper'] - df_sorted['explain_upper']
# df_sorted['HU-CR'] = df_sorted['human_upper'] - df_sorted['create_upper']
# df_sorted['CO-EX'] = df_sorted['continue_upper'] - df_sorted['explain_upper']
# df_sorted['CO-CR'] = df_sorted['continue_upper'] - df_sorted['create_upper']
# df_sorted['EX-CR'] = df_sorted['explain_upper'] - df_sorted['create_upper']

# Calculate absolute differences in the reverse order
df_sorted['HU-CO'] = df_sorted['continue_upper'] - df_sorted['human_upper']
df_sorted['HU-EX'] = df_sorted['explain_upper'] - df_sorted['human_upper']
df_sorted['HU-CR'] = df_sorted['create_upper'] - df_sorted['human_upper']
df_sorted['CO-EX'] = df_sorted['explain_upper'] - df_sorted['continue_upper']
df_sorted['CO-CR'] = df_sorted['create_upper'] - df_sorted['continue_upper']
df_sorted['EX-CR'] = df_sorted['create_upper'] - df_sorted['explain_upper']


# Select only the required columns
df_final = df_sorted[['connective', 'human_upper', 'HU-CO', 'HU-EX', 'HU-CR', 'CO-EX', 'CO-CR', 'EX-CR']]

# write the data to a new CSV file
df_final.to_csv("../results/connectives_upper_pubmed_de_diffs.csv", index=False)

# ##############################################################################
# # make a heatmap
# ##############################################################################

sns.set_theme(style="white")

# Use the first 10 rows
data = df_final.iloc[:30]

# Make heat map for the values in the columns HU-CO, HU-EX, HU-CR
data = data.set_index('connective')

# Rename specific columns for the heatmap
data = data.rename(columns={'HU-CO': 'human-continue', 'HU-EX': 'human-explain', 'HU-CR': 'human-create', 'human-upper': 'human_upper'})

# Create a mask for the heatmap where human_upper column is set to NaN
mask = data.copy()
mask['human_upper'] = np.nan

# Set the size of the plot
plt.figure(figsize=(8, 8))

# Create a heatmap with the mask for color mapping but with original data for annotation
ax = sns.heatmap(data=mask[['human_upper', 'human-continue', 'human-explain', 'human-create']], 
                 annot=data[['human_upper', 'human-continue', 'human-explain', 'human-create']], fmt="d", 
                 linewidths=.3, cbar=False, cmap="YlGnBu", annot_kws={"size": 20}, xticklabels=False)

# Make the background transparent
ax.set_facecolor('none')
plt.gcf().set_facecolor('none')

# Set the font size of the y-axis labels
plt.yticks(fontsize=20)

# Place the x-axis labels on the top
ax.xaxis.tick_top()

# Set font size for the labels
ax.tick_params(labelsize=20)

# Remove the y-axis label
plt.ylabel("")

# Correctly position the values in the human_upper column
for i in range(data.shape[0]):
    ax.text(0.5, i + 0.5, f'{data["human_upper"].iloc[i]:.0f}', 
            ha='center', va='center', color='black', fontsize=20)
# Set the title of the plot

# Save the plot with a transparent background
plt.savefig('../../viz/for_paper/connectives_cap_pubmed_de_heatmap.pdf', bbox_inches='tight', transparent=True)
plt.savefig('../../viz/for_paper/connectives_cap_pubmed_de_heatmap.png', bbox_inches='tight', transparent=True)

# Show the plot
plt.show()
plt.close()



