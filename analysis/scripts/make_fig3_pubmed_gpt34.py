import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

# ##############################################################################
# # create a csv file with the differences between the usage of capitalized
# # connectives in the human and the gpt-3 texts for the top 30 connectives
# # produces Figure 1
# ##############################################################################

# Read the data from the CSV file into a DataFrame
df3 = pd.read_csv(f"../../feature_extraction/2309gpt3/results/connectives/connectives_all_pubmed_de.csv")
df4 = pd.read_csv(f"../../feature_extraction/2403gpt4/results/connectives/connectives_all_pubmed_de.csv")
df42 = pd.read_csv(f"../../feature_extraction/2409gpt4/results/connectives/connectives_all_pubmed_de.csv")


# First merge: between df3 and df4
dfm = pd.merge(df3, df4, on=["connective"], suffixes=('_gpt3', '_gpt4'))

# Check column names to ensure the merge went as expected
print("Columns after first merge:", dfm.columns.tolist())

# Second merge: between dfm and df42
# Since 'human_upper' also appears in df42, you need to include it in the merge and apply suffixes correctly
df = pd.merge(dfm, df42, on=["connective"], suffixes=('', '_gpt42'))

# Check column names to ensure the merge went as expected
print("Columns after second merge:", df.columns.tolist())

# Sort the DataFrame based on 'human_upper' column in descending order and select the top rows
df_sorted = df.sort_values(by='human_upper_gpt3', ascending=False).head(30)


print(df_sorted.head())

# Calculate absolute differences in the reverse order
df_sorted['HU-CO 4'] = df_sorted['continue_upper_gpt4'] - df_sorted['human_upper_gpt3']
df_sorted['HU-EX 4'] = df_sorted['explain_upper_gpt4'] - df_sorted['human_upper_gpt3']
df_sorted['HU-CR 4'] = df_sorted['create_upper_gpt4'] - df_sorted['human_upper_gpt3']
df_sorted['HU-CO 3'] = df_sorted['continue_upper_gpt3'] - df_sorted['human_upper_gpt3']
df_sorted['HU-EX 3'] = df_sorted['explain_upper_gpt3'] - df_sorted['human_upper_gpt3']
df_sorted['HU-CR 3'] = df_sorted['create_upper_gpt3'] - df_sorted['human_upper_gpt3']
df_sorted['HU-CO 42'] = df_sorted['ashuman_upper'] - df_sorted['human_upper_gpt3']
df_sorted['HU-EX 42'] = df_sorted['asmachine_upper'] - df_sorted['human_upper_gpt3']


# # Select only the required columns
df_final = df_sorted[['connective', 'human_upper_gpt3', 'HU-CO 3', 'HU-EX 3', 'HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4', 'HU-CO 42', 'HU-EX 42']]

# drop the rows with NaN values
df_final = df_final.dropna()

# convert HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4' to integers
df_final['HU-CO 4'] = df_final['HU-CO 4'].astype(int)
df_final['HU-EX 4'] = df_final['HU-EX 4'].astype(int)
df_final['HU-CR 4'] = df_final['HU-CR 4'].astype(int)
df_final['HU-CO 42'] = df_final['HU-CO 42'].astype(int)
df_final['HU-EX 42'] = df_final['HU-EX 42'].astype(int)

# print(df_final)

# # ##############################################################################
# # # make a heatmap with Matplotlib
# # ##############################################################################

# select only the top 30 human connectives where system is gpt3 and gpt4
data = df_final.iloc[:30]

print(data)

# Prepare the data for imshow
human_data = data[['human_upper_gpt3']].values.flatten()  # 'Human' row data
heatmap_data = data[['HU-CO 3', 'HU-EX 3', 'HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4', 'HU-CO 42', 'HU-EX 42']].values.T  

# Define the connectives (x-axis labels)
connectives = data['connective'].values

# Define row labels
row_labels = ['Human', 'Continue', 'Explain', 'Create', 'Continue', 'Explain', 'Create', 'AsHuman', 'AsMachine']

# Set the size of the plot
fig, ax = plt.subplots(figsize=(16, 10))

# Normalize colors with TwoSlopeNorm to center at zero
vmin, vmax = heatmap_data.min(), heatmap_data.max()
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Create a heatmap for non-human rows only (rows 1 to 6)
cax = ax.imshow(heatmap_data, cmap='coolwarm', aspect='auto', norm=norm)

# Add color bar for reference
# plt.colorbar(cax)

# Set the ticks and labels for the x and y axes
ax.set_xticks(np.arange(len(connectives)))
# make ticks invisible
ax.tick_params(axis='x', which='both', bottom=False, top=False)
ax.set_xticklabels(connectives, fontsize=20, rotation=45, ha='right') 
# make ticks invisible
ax.tick_params(axis='y', which='both', left=False, right=False)
ax.set_yticks(np.arange(8))  # Only for the heatmap data (3 rows)
ax.set_yticklabels(row_labels[1:], fontsize=20)
# add one more tick and label for the 'Human' row
# ax.set_yticks(np.arange(4)-0.5, minor=True)
# ax.set_yticklabels(row_labels, fontsize=20, minor=True)

# Overlay the 'Human' row values as text separately above the heatmap
for i in range(len(connectives)):
    value = human_data[i]
    ax.text(i, -0.8, f'{value:.0f}', ha='center', va='center', color='dimgray', fontsize=18)

# Annotate each cell with the numeric value for heatmap data
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        ax.text(j, i, '{:.0f}'.format(heatmap_data[i, j]), ha='center', va='center', color='black', fontsize=18)

# Adjust layout for better appearance
plt.subplots_adjust(left=0.15, right=0.95, top=0.85, bottom=0.3)

# Remove any unnecessary spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
# extend the left spine up
ax.spines['left'].set_bounds(-0.5, 2.5)
ax.spines['left'].set_visible(False)

# add black line between the two systems, between rows 3 and 4
ax.axhline(y=2.5, color='black', linewidth=2)
ax.axhline(y=5.5, color='black', linewidth=2)


plt.tight_layout()

# # Save the plot
plt.savefig('../../viz/for_paper/connectives_cap_pubmed_de_heatmap_gpt34.pdf', format='pdf', bbox_inches='tight')

# # Show the plot
plt.show()

# # merge the two dataframes on 'connective' and 'human_upper'
# df = pd.merge(df3, df4, on=['connective'], suffixes=('_gpt3', '_gpt4'))

# # Sort the DataFrame based on the 'human_upper' column in descending order and select the top 30 rows
# df_sorted = df.sort_values(by='human_upper_gpt3', ascending=False)

# print(df_sorted.head())

# # Calculate absolute differences in the reverse order
# df_sorted['HU-CO 4'] = df_sorted['continue_upper_gpt4'] - df_sorted['human_upper_gpt3']
# df_sorted['HU-EX 4'] = df_sorted['explain_upper_gpt4'] - df_sorted['human_upper_gpt3']
# df_sorted['HU-CR 4'] = df_sorted['create_upper_gpt4'] - df_sorted['human_upper_gpt3']
# df_sorted['HU-CO 3'] = df_sorted['continue_upper_gpt3'] - df_sorted['human_upper_gpt3']
# df_sorted['HU-EX 3'] = df_sorted['explain_upper_gpt3'] - df_sorted['human_upper_gpt3']
# df_sorted['HU-CR 3'] = df_sorted['create_upper_gpt3'] - df_sorted['human_upper_gpt3']


# # # Select only the required columns
# df_final = df_sorted[['connective', 'human_upper_gpt3', 'HU-CO 3', 'HU-EX 3', 'HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4']]

# # drop the rows with NaN values
# df_final = df_final.dropna()

# # convert HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4' to integers
# df_final['HU-CO 4'] = df_final['HU-CO 4'].astype(int)
# df_final['HU-EX 4'] = df_final['HU-EX 4'].astype(int)
# df_final['HU-CR 4'] = df_final['HU-CR 4'].astype(int)

# # print(df_final)

# # # ##############################################################################
# # # # make a heatmap with Matplotlib
# # # ##############################################################################

# # select only the top 30 human connectives where system is gpt3 and gpt4
# data = df_final.iloc[:30]

# print(data)

# # Prepare the data for imshow
# human_data = data[['human_upper_gpt3']].values.flatten()  # 'Human' row data
# heatmap_data = data[['HU-CO 3', 'HU-EX 3', 'HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4']].values.T  
