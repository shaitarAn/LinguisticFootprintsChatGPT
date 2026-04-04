import json

def find_features_in_json(json_file, feature_list, domain):
    # Load JSON data from a file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Dictionary to store results: {feature: {category: index}}
    feature_indices = {}

    # Loop through each key in the JSON data
    for key, value in data.items():
        if "human" in key and "bon" in value:  
            for feature in feature_list:
                if feature in value["bon"]:  
                    if feature not in feature_indices:
                        feature_indices[feature] = {}
                        # print(f"{feature} not in {key}")
                    feature_indices[feature][key] = value["bon"].index(feature)
                    print()
                    print(feature)
                    print(domain, ":", key, value["bon"].index(feature)+1, "/", len(value["bon"]))

    return feature_indices

# List of features to search for English
features_to_search_English = ["dependency_distance_mean", "connectives", "prop_pos_SCONJ", "prop_pos_PRON"]

# List of features to search for German
features_to_search_German = ["sentence_length_mean", "prop_pos_ADV", "prop_pos_PRON", "fresch_reading_ease"]

domain = 'clinical'
language = 'german'

print(language, domain)

if language == 'english':
    # Path to the JSON file
    json_file_path = f'../results/2403gpt4_english_{domain}_significant_features_0.01.json'
    # Call the function and print the results
    results = find_features_in_json(json_file_path, features_to_search_English, domain)

else:
    # Path to the JSON file
    json_file_path = f'../results/2403gpt4_german_{domain}_significant_features_0.01.json'
    # Call the function and print the results
    results = find_features_in_json(json_file_path, features_to_search_German, domain)





# feats = ['sentence_length_mean', 'dependency_distance_mean', 'coleman_liau_index', 'adverbs']