import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

# ##############################################################################
# # create a csv file with the differences between the usage of capitalized
# # connectives in the human and the gpt-3 texts for the top 30 connectives
# # produces Figure 1
# ##############################################################################

data_run = '2309gpt3'

# Read the data from the CSV file into a DataFrame
df = pd.read_csv(f"../../feature_extraction/{data_run}/results/connectives/connectives_all_pubmed_de.csv")

# Sort the DataFrame based on the 'human_upper' column in descending order and select the top 30 rows
df_sorted = df.sort_values(by='human_upper', ascending=False)

# Calculate absolute differences in the reverse order
df_sorted['HU-CO'] = df_sorted['continue_upper'] - df_sorted['human_upper']
df_sorted['HU-EX'] = df_sorted['explain_upper'] - df_sorted['human_upper']
df_sorted['HU-CR'] = df_sorted['create_upper'] - df_sorted['human_upper']
df_sorted['CO-EX'] = df_sorted['explain_upper'] - df_sorted['continue_upper']
df_sorted['CO-CR'] = df_sorted['create_upper'] - df_sorted['continue_upper']
df_sorted['EX-CR'] = df_sorted['create_upper'] - df_sorted['explain_upper']

# Select only the required columns
df_final = df_sorted[['connective', 'human_upper', 'HU-CO', 'HU-EX', 'HU-CR', 'CO-EX', 'CO-CR', 'EX-CR']]

# drop the rows with NaN values
df_final = df_final.dropna()
# convert HU-CR 3', 'HU-CO 4', 'HU-EX 4', 'HU-CR 4' to integers
df_final['HU-CO'] = df_final['HU-CO'].astype(int)
df_final['HU-EX'] = df_final['HU-EX'].astype(int)
df_final['HU-CR'] = df_final['HU-CR'].astype(int)
# ##############################################################################
# # make a heatmap with Matplotlib
# ##############################################################################

data = df_final.iloc[:30]

print(data)

# Prepare the data for imshow
human_data = data[['human_upper']].values.flatten()  # 'Human' row data
heatmap_data = data[['HU-CO', 'HU-EX', 'HU-CR']].values.T  

# Define the connectives (x-axis labels)
connectives = data['connective'].values

# Define row labels
row_labels = ['Human', 'Continue', 'Explain', 'Create']

# Set the size of the plot
fig, ax = plt.subplots(figsize=(16, 5))

# Normalize colors with TwoSlopeNorm to center at zero
vmin, vmax = heatmap_data.min(), heatmap_data.max()
norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

# Create a heatmap for 'HU-CO', 'HU-EX', 'HU-CR' only (rows 1 to 3)
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
ax.set_yticks(np.arange(3))  # Only for the heatmap data (3 rows)
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

plt.tight_layout()

# Save the plot
# plt.savefig(f'../../viz/for_paper/connectives_cap_pubmed_de_{data_run}.pdf', format='pdf', bbox_inches='tight')

# Show the plot
plt.show()
