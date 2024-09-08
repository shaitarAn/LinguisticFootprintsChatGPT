import pandas as pd
import os
import argparse
import yaml

def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def parse_args():
    parser = argparse.ArgumentParser(description="Process morphological and lexical features.")
    parser.add_argument("-f", "--feature", type=str, required=True, help="Type of feature to convert (morphology or lexical_richness).")
    parser.add_argument("-o", "--output_dir", type=str, required=True, help="Base directory for results output.")
    parser.add_argument("-c", "--config", type=str, required=True, help="Path to YAML configuration file.")
    return parser.parse_args()

def transform_data(df, feature):
    # print(feature)
    df_pivot = df.pivot(index='file', columns='system', values=[feature])
    df_pivot.columns = [col[1] for col in df_pivot.columns]
    df_pivot.reset_index(inplace=True)
    df_pivot.drop(columns=['file'], inplace=True)
    # print(df_pivot.head())
    return df_pivot

def process_data(args, config):
    domain_dfs = {}
    language_dfs = {}

    features = {}
    corpora = config['corpora']['german'] + config['corpora']['english'] if args.feature == "lexical_richness" else config['corpora']['german']
    if args.feature == "morphology":
        features = {'shannon':'shannon_entropy', 'simpson':'simpson_diversity'}
    else:
        features = {'MTLD':'mtld', 'TTR': 'type_token_ratio', 'Yules': 'yules_k'}

    for corpus in corpora:
        df = pd.read_csv(f"{args.output_dir}/{args.feature}/{corpus}.csv")
        language = 'german' if corpus in config['corpora']['german'] else 'english'

        for feature, feature_name in features.items():  
            transformed_df = transform_data(df, feature)
            feature_dir = f"{args.output_dir}/per_feature/{feature_name}"
            os.makedirs(feature_dir, exist_ok=True)
            transformed_df.to_csv(f"{feature_dir}/{corpus}.csv", index=False)

            # Aggregate data by domain
            for domain, domain_corpora in config['domains'].items():
                if corpus in domain_corpora:
                    domain_key = (domain, language, feature_name)
                    if domain_key not in domain_dfs:
                        domain_dfs[domain_key] = transformed_df.copy()
                    else:
                        domain_dfs[domain_key] = pd.concat([domain_dfs[domain_key], transformed_df], ignore_index=True)

            # Aggregate data by language
            language_key = (language, feature_name)
            if language_key not in language_dfs:
                language_dfs[language_key] = transformed_df.copy()
            else:
                language_dfs[language_key] = pd.concat([language_dfs[language_key], transformed_df], ignore_index=True)

    # Write domain aggregated data
    for (domain, language, feature_name), df in domain_dfs.items():
        domain_dir = f"{args.output_dir}/per_domain/{domain}/{language}"
        os.makedirs(domain_dir, exist_ok=True)
        df.to_csv(f"{domain_dir}/{feature_name}.csv", index=False)

    # Write language aggregated data
    for (language, feature_name), df in language_dfs.items():
        language_dir = f"{args.output_dir}/per_language/{language}"
        os.makedirs(language_dir, exist_ok=True)
        df.to_csv(f"{language_dir}/{feature_name}.csv", index=False)


def main():
    args = parse_args()
    config = load_config(args.config)
    process_data(args, config)

if __name__ == "__main__":
    main()
