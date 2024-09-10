import pandas as pd
import os, sys
import yaml
from features_list import features_to_visualize_dict

def load_config(config_path):
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def main(output_dir, config_path):
    config = load_config(config_path)

    # Retrieve configuration data
    tasks = config['tasks']
    corpora_by_language = {
        'german': config['corpora'].get('german', []),
        'english': config['corpora'].get('english', [])
    }
    domains = config['domains']

    # Initialize dictionaries to hold dataframes
    language_dicts = {language: {} for language in corpora_by_language}
    domain_dicts = {domain: {language: {} for corpus_list in domains.values() for language in corpora_by_language if corpus_list} for domain in domains}

    for language, corpora in corpora_by_language.items():
        for corpus in corpora:
            csv_directory = os.path.join(output_dir, 'results', 'per_corpus', corpus)
            print(f"Processing {corpus} ({language}) in {csv_directory}")

            try:
                for file_name in os.listdir(csv_directory):
                    df = pd.read_csv(os.path.join(csv_directory, file_name))
                    features_in_file = df.iloc[:, 0].tolist()

                    for feature in features_in_file:
                        if feature in features_to_visualize_dict:
                            feature_data = df[df.iloc[:, 0] == feature].iloc[:, 1:]  # drop the first column
                            feature_data = feature_data[tasks]  # reorder columns based on tasks

                            # Append to the language specific dictionary
                            if feature not in language_dicts[language]:
                                language_dicts[language][feature] = [feature_data]
                            else:
                                language_dicts[language][feature].append(feature_data)

                            # Append to the domain specific dictionary
                            for domain, corpora_list in domains.items():
                                if corpus in corpora_list:
                                    if feature not in domain_dicts[domain][language]:
                                        domain_dicts[domain][language][feature] = [feature_data]
                                    else:
                                        domain_dicts[domain][language][feature].append(feature_data)

            except Exception as e:
                print(f"Error processing {corpus}: {e}")

    # Save results
    for language, features_dict in language_dicts.items():
        for feature, dataframes in features_dict.items():
            combined_df = pd.concat(dataframes, ignore_index=True)
            path = os.path.join(output_dir, 'results', 'per_language', language, f"{feature}.csv")
            os.makedirs(os.path.dirname(path), exist_ok=True)
            combined_df.to_csv(path, index=False)

    for domain, lang_features in domain_dicts.items():
        for language, features_dict in lang_features.items():
            for feature, dataframes in features_dict.items():
                combined_df = pd.concat(dataframes, ignore_index=True)
                path = os.path.join(output_dir, 'results', 'per_domain', domain, language, f"{feature}.csv")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                combined_df.to_csv(path, index=False)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])