import pandas as pd
import os
import scipy.stats as stats
import sys

sys.path.append('../../feature_extraction/scripts/')
from features_list import features_to_visualize_dict

def load_data(metric, path_to_data, language):
    file_paths = [
        os.path.join(path_to_data, f"2309gpt3/results/per_language/{language}", f"{metric}.csv"),
        os.path.join(path_to_data, f"2403gpt4/results/per_language/{language}", f"{metric}.csv")
    ]
    df_gpt3 = pd.read_csv(file_paths[0])
    df_gpt4 = pd.read_csv(file_paths[1])
    df_gpt3['dataset'] = 'GPT3'
    df_gpt4['dataset'] = 'GPT4'
    combined_df = pd.concat([df_gpt3, df_gpt4])
    return combined_df

def perform_statistical_tests(path_to_data, language, feature):
    # feats_to_check = ["entropy", "sentence_length_mean", "proportion_unique_tokens",
    #                   "token_length_mean", "flesch_reading_ease", "pos_prop_ADJ",
    #                   "pos_prop_CCONJ", "pos_prop_NOUN", "mtld"]  # List of metrics to check

    results = {}
    for metric in features_to_visualize_dict:
        try:
            df = load_data(metric, path_to_data, language)
            continue_gpt3 = df[df['dataset'] == 'GPT3'][feature]
            continue_gpt4 = df[df['dataset'] == 'GPT4'][feature]

            # Perform the Mann-Whitney U test
            u_stat, p_value = stats.mannwhitneyu(continue_gpt3, continue_gpt4, alternative='two-sided')

            results[metric] = {
                'U statistic': u_stat,
                'P value': p_value
            }
        except FileNotFoundError:
            print(f"Could not find data for {metric}")

    return results

def main():
    path_to_data = "../../feature_extraction/"
    language = "german"
    task = "continue"  # The feature across which to compare distributions

    test_results = perform_statistical_tests(path_to_data, language, task)
    count_all = 0
    count_significant = 0
    for metric, result in test_results.items():
        count_all += 1
        if result['P value'] < 0.01:
            count_significant += 1
            print(f"{metric}: U statistic = {result['U statistic']}, P value = {result['P value']} (significant)")
        # print(f"{metric}: U statistic = {result['U statistic']}, P value = {result['P value']}")
    print()
    print(language, task)
    print(f"Total number of metrics: {count_all}")
    print(f"Number of significant results: {count_significant}")

if __name__ == "__main__":
    main()
