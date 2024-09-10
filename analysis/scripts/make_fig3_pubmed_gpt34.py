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

# Group definitions by corpus
groups = {
    'GPT-3, 2023': ['HU-CO 3', 'HU-EX 3', 'HU-CR 3'],
    'GPT-4, 2024': ['HU-CO 4', 'HU-EX 4', 'HU-CR 4'],
}

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
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

# Assuming df_final has been properly formatted and calculated as previously detailed

# Select only the top 30 entries
data = df_final.iloc[:30]
print(data)

# Data preparation for the heatmap
human_data = data['human_upper_gpt3'].values.flatten()  # Human data for annotation
heatmap_data = data[['HU-CO 3', 'HU-EX 3', 'HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4', 'HU-CO 42', 'HU-EX 42']].values.T

# Set the connectives and labels
connectives = data['connective'].values
row_labels = ['Continue', 'Explain', 'Create', 'Continue', 'Explain', 'Create', 'AsHuman', 'AsMachine']

# Set up the figure and axes
fig, ax = plt.subplots(figsize=(18, 10))
norm = TwoSlopeNorm(vmin=heatmap_data.min(), vcenter=0, vmax=heatmap_data.max())
cax = ax.imshow(heatmap_data, cmap='coolwarm', aspect='auto', norm=norm)

# Configure tick labels
ax.set_xticks(np.arange(len(connectives)))
ax.set_xticklabels(connectives, fontsize=20, rotation=45, ha='right')
ax.set_yticks(np.arange(len(row_labels)))
ax.set_yticklabels(row_labels, fontsize=18)

# Annotate the 'Human' row values separately above the heatmap
for i in range(len(connectives)):
    ax.text(i, -0.8, f'{int(human_data[i]):d}', ha='center', va='center', color='dimgray', fontsize=18)

# Annotate each cell with its numeric value
for i in range(heatmap_data.shape[0]):
    for j in range(heatmap_data.shape[1]):
        text_color = 'white' if abs(heatmap_data[i, j]) > norm.vmax / 2 else 'black'
        ax.text(j, i, f'{int(heatmap_data[i, j]):d}', ha='center', va='center', color=text_color, fontsize=18)

# Visual adjustments for axis visibility
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)

# Manually set the axes position
# fig.subplots_adjust(left=0.27)  # Adjust this value as needed
# ax.set_position([0.25, 0.1, 0.65, 0.8])  # [left, bottom, width, height] in figure coordinate

# Add bold and vertical group labels further to the left
group_labels = ['GPT-3', 'GPT-4']
group_positions = [1, 5]  # Adjust these positions to match the middle of your groups
for label, pos in zip(group_labels, group_positions):
    ax.text(-3, pos, label, fontsize=18, ha='right', va='center', rotation=90, fontweight='bold')


# Draw lines to separate the groups
ax.axhline(y=2.5, color='black', linewidth=2)  # Between GPT-3 and GPT-4 groups
ax.axhline(y=5.5, color='black', linewidth=2)  # Between GPT-4 and AsHuman groups

# Improve layout to handle tight spacing and save the figure
plt.tight_layout()
plt.savefig('../../viz/for_paper/connectives_cap_pubmed_de_heatmap_gpt34.pdf', format='pdf', bbox_inches='tight')
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
