import json
from collections import Counter
import sys
sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

language = "english"
generation = f"2309gpt3"
domain = "science" # "news" or "clinical"
# Load the JSON data from a file
with open(f'../results/{generation}_english_german_significant_features_0.01.json', 'r') as file:
    significant_features = json.load(file)

# Define the pairs to look at (involving 'human')
relevant_pairs = ['human-continue', 'human-explain', 'human-create']
print(generation)

from collections import defaultdict

# Initialize a dictionary to tally feature significance with position consideration
feature_scores = defaultdict(float)

# Adjust the weight of a feature based on its position in the list
for pair in relevant_pairs:
    if pair in significant_features:
        features = significant_features[pair]['bon']
        # print()
        # print(f"Features for {pair}: {features[:8]}")
        total_features = len(features)
        for index, feature in enumerate(features):
            # Decrease the score increment as the feature appears later in the list
            # For example, give higher score to features that appear earlier
            score = (total_features - index) / total_features
            feature_scores[feature] += score

# Now convert scores to a sorted list to find the top weighted features
sorted_features = sorted(feature_scores.items(), key=lambda x: x[1], reverse=True)
top_weighted_features = [i for i, _ in sorted_features]

# Print the results
# print("Top 5 weighted significant features across all human-involved text pairs in 'bon':")
print(top_weighted_features)
# for i in top_weighted_features:
#     try:
#         print(" ".join(features_to_visualize_dict[i].split(" ")[1:]).strip())
#         # print(features_to_visualize_dict[i].split(" ")[0].strip())
#     except KeyError:
#         print(" ".join(i.split(" ")[1:]))

from collections import Counter

# List of feature groups, each as a string of comma-separated feature names
feature_groups = [
    # german
    "pos_prop_PUNCT, alpha_ratio, dependency_distance_std, mean_word_length, prop_adjacent_dependency_relation_mean",
    "MTLD, mean_word_length, alpha_ratio, pos_prop_ADJ, prop_adjacent_dependency_relation_mean",
    "proportion_unique_tokens, sentence_length_std, TTR, alpha_ratio, duplicate_ngram_chr_fraction_5",
    "MTLD, pos_prop_PUNCT, pos_prop_VERB, alpha_ratio, Yules",
    "pos_prop_VERB, pos_prop_PUNCT, alpha_ratio, sentence_length_std, dependency_distance_std",
    "MTLD, pos_prop_VERB, alpha_ratio, pos_prop_PUNCT, Yules",
    # english
    "mean_word_length, token_length_mean, coleman_liau_index, syllables_per_token_mean, syllables_per_token_std",
    "MTLD, entropy, mean_word_length, coleman_liau_index, token_length_mean",
    "MTLD, mean_word_length, pos_prop_VERB, prop_adjacent_dependency_relation_mean, dependency_distance_std",
    "MTLD, mean_word_length, TTR, coleman_liau_index, proportion_unique_tokens",
    "coleman_liau_index, lix, mean_word_length, token_length_mean, flesch_reading_ease",
    "lix, automated_readability_index, coleman_liau_index, mean_word_length, flesch_reading_ease"
]

feature_groups = [
    # gpt3
    "pos_prop_PUNCT, alpha_ratio, dependency_distance_std, mean_word_length, prop_adjacent_dependency_relation_mean",
    "proportion_unique_tokens, sentence_length_std, TTR, alpha_ratio, duplicate_ngram_chr_fraction_5",    
    "pos_prop_VERB, pos_prop_PUNCT, alpha_ratio, sentence_length_std, dependency_distance_std",
    "mean_word_length, token_length_mean, coleman_liau_index, syllables_per_token_mean, syllables_per_token_std",
    "MTLD, mean_word_length, pos_prop_VERB, prop_adjacent_dependency_relation_mean, dependency_distance_std",
    "coleman_liau_index, lix, mean_word_length, token_length_mean, flesch_reading_ease",

    # gpt4
    "MTLD, mean_word_length, alpha_ratio, pos_prop_ADJ, prop_adjacent_dependency_relation_mean",
    "MTLD, pos_prop_PUNCT, pos_prop_VERB, alpha_ratio, Yules",
    "MTLD, pos_prop_VERB, alpha_ratio, pos_prop_PUNCT, Yules",
    "MTLD, entropy, mean_word_length, coleman_liau_index, token_length_mean",
    "MTLD, mean_word_length, TTR, coleman_liau_index, proportion_unique_tokens",
    "lix, automated_readability_index, coleman_liau_index, mean_word_length, flesch_reading_ease"
]

# Initialize a Counter to count feature occurrences
feature_counts = Counter()

# Process each group of features
for group in feature_groups:
    # Split the group into individual features and strip any surrounding whitespace
    features = [features_to_visualize_dict.get(feature.strip(), feature.strip()) for feature in group.split(',')]

    # Update the counter with these features
    feature_counts.update(features)

# Convert the counter to a dictionary
feature_dictionary = dict(feature_counts)

# sort the dictionary by the number of occurrences
feature_dictionary = dict(sorted(feature_dictionary.items(), key=lambda item: item[1], reverse=True))

# Display the resulting dictionary of features and their occurrences
# print(feature_dictionary)

