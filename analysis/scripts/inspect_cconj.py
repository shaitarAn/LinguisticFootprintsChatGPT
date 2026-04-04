import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

corpus = 'cs_de'
FEATURE = 'pos_prop_PRON'
# Directory containing the CSV files
input_directory = f"../../feature_extraction/2403gpt4/results/per_corpus/{corpus}"

# Initialize a list to collect results
results_list = []

# Iterate over all CSV files in the directory
for filename in os.listdir(input_directory):
    if filename.endswith('.csv'):
        file_path = os.path.join(input_directory, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path, index_col=0)
        
        # Check if 'pos_prop_CCONJ' row exists in the DataFrame
        if FEATURE in df.index:
            # Extract the row for 'pos_prop_CCONJ'
            pos_prop_cconj_row = df.loc[FEATURE]
            
            # Extract the file number from the filename for sorting
            try:
                file_number = int(''.join(filter(str.isdigit, filename)))
            except ValueError:
                continue  # Skip files where the filename doesn't contain a number
            
            # Create a dictionary with the filename and the values
            new_row = {
                'filename': file_number,
                'human': pos_prop_cconj_row['human'],
                'continue': pos_prop_cconj_row['continue'],
                'explain': pos_prop_cconj_row['explain'],
                'create': pos_prop_cconj_row['create']
            }
            
            # Append the new row to the results list
            results_list.append(new_row)

# Convert the list to a DataFrame
results_df = pd.DataFrame(results_list)

# Sort results_df by filename in ascending order
results_df = results_df.sort_values(by='filename')

# Convert relevant columns to numeric, forcing errors to NaN and then handling them
numeric_columns = ['human', 'continue', 'explain', 'create']
for col in numeric_columns:
    results_df[col] = pd.to_numeric(results_df[col], errors='coerce')

# Check for and handle any NaN values if necessary (e.g., remove rows with NaN)
results_df = results_df.dropna(subset=numeric_columns)

# Sort results_df by filename in ascending order
results_df['filename'] = results_df['filename'].astype(int)  # Ensure filename is treated as numeric for sorting
results_df = results_df.sort_values(by='filename')

# Create a plot
plt.figure(figsize=(12, 6))

# Plot regression lines for each category
sns.regplot(x='filename', y='human', data=results_df, scatter=False, label='Human', color='blue', line_kws={'linestyle': '--'})
sns.regplot(x='filename', y='continue', data=results_df, scatter=False, label='Continue', color='green', line_kws={'linestyle': '--'})
sns.regplot(x='filename', y='explain', data=results_df, scatter=False, label='Explain', color='orange', line_kws={'linestyle': '--'})
sns.regplot(x='filename', y='create', data=results_df, scatter=False, label='Create', color='red', line_kws={'linestyle': '--'})

# Add labels and title
plt.xlabel('File Number')
plt.ylabel('Proportion')
plt.title(f'Regression Lines for {FEATURE} in {corpus}')

# Set y-axis limits and ticks for better readability
plt.ylim(0, results_df[numeric_columns].max().max() + 0.01)  # Set y-axis limit slightly above max value
plt.yticks([round(i, 2) for i in plt.yticks()[0]])  # Round the y-axis tick labels to 2 decimal places

# Set x-axis ticks to be less cluttered
plt.xticks(results_df['filename'][::2], rotation=45, ha='right')  # Show every second x-tick for better spacing

plt.legend()

# Show grid
plt.grid(True)

# Display the plot
plt.tight_layout()
# # Save the plot
plt.savefig(f'../../viz/{FEATURE}_{corpus}.png', dpi=300)
plt.show()




