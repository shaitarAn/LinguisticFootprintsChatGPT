import pandas as pd
from collections import defaultdict

generation_name = "2403gpt4"

# Assuming 'df' is your DataFrame with the data shown earlier
data = f'../results/{generation_name}_english_german_stats_0.01.csv'

# read csv file

df = pd.read_csv(data)

# Define the relevant pairs involving 'human'
relevant_pairs = ['human-continue', 'human-explain', 'human-create']

if generation_name == "2309gpt3":
    interested_features = ['alpha_ratio', 'pos_prop_PUNCT', 'token_length_median', 'dependency_distance_std', 'prop_adjacent_dependency_relation_mean', 'sentence_length_std', 'mean_word_length', 'mtld', 'lix', 'second_order_coherence']
else:
    interested_features = ['mtld', 'yules_k', 'alpha_ratio', 'pos_prop_PUNCT', 'token_length_median', 'type_token_ratio', 'prop_adjacent_dependency_relation_mean', 'mean_word_length', 'lix', 'automated_readability_index']


# Filter the DataFrame for relevant pairs and features
df_filtered = df[df['persona'].isin(relevant_pairs) & df['feature'].isin(interested_features)]

# Initialize dictionary to hold cumulative statistics
feature_stats = defaultdict(lambda: {'t-statistic': [], 'p-value': [], 'bon': []})

# Populate the dictionary with data from the DataFrame
for index, row in df_filtered.iterrows():
    feature_stats[row['feature']]['t-statistic'].append(row['t-statistic'])
    feature_stats[row['feature']]['p-value'].append(row['pvalue'])
    feature_stats[row['feature']]['bon'].append(row['bon'])

# Compute averages and prepare the final DataFrame
results_data = {
    'feature': [],
    'average_t-statistic': [],
    'average_p-value': [],
    'average_bon': []
}

for feature, stats in feature_stats.items():
    results_data['feature'].append(feature)
    results_data['average_t-statistic'].append(sum(stats['t-statistic']) / len(stats['t-statistic']))
    results_data['average_p-value'].append(sum(stats['p-value']) / len(stats['p-value']))
    results_data['average_bon'].append(sum(stats['bon']) / len(stats['bon']))

df_results = pd.DataFrame(results_data)

# Print or save the results
print(df_results)
# Optionally save to a CSV
# df_results.to_csv('feature_analysis_results.csv', index=False)

