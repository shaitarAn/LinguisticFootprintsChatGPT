import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

language = 'de'
generation = 'data_2403gpt4' # 'data_2309gpt3' or 'data_2403gpt4'

df = pd.read_csv(f"../../feature_extraction/{generation.split('_')[1]}/results/connectives/connectives_all_pubmed_{language}.csv")

token_counts = {
    "data_2309gpt3": {
        "pubmed_en": {"explain_upper": 74766, "continue_upper": 70133, "create_upper": 66598, "human_upper": 95062},
        "pubmed_de": {"explain_upper": 68933, "continue_upper": 77869, "create_upper": 73737, "human_upper": 66573},
    },
    "data_2403gpt4": {
        "pubmed_en": {"explain_upper": 72788, "continue_upper": 64553, "create_upper": 60144, "human_upper": 78915},
        "pubmed_de": {"explain_upper": 57274, "continue_upper": 58718, "create_upper": 62685, "human_upper": 66573},
    }
}

print(token_counts)


# Normalize the _upper columns to occurrences per 1,000 tokens
normalized_df = df[['connective', 'explain_upper', 'continue_upper', 'create_upper', 'human_upper']].copy()
for col in ['explain_upper', 'continue_upper', 'create_upper', 'human_upper']:
    normalized_df[col] = (normalized_df[col] / token_counts[generation][f"pubmed_{language}"][col]) * 10000

# Display the resulting DataFrame
print(normalized_df)

# Save the normalized DataFrame to a new CSV file
normalized_df.to_csv(f"../../feature_extraction/2403gpt4/results/connectives/connectives_upper_pubmed_{language}_normalized.csv", index=False)

normalized_df = normalized_df[(normalized_df[['explain_upper', 'continue_upper', 'create_upper', 'human_upper']] >= 1).any(axis=1)]
# remove rows with empty values
normalized_df = normalized_df.dropna()

# Set the 'connective' column as the index for visualization
normalized_df.set_index('connective', inplace=True)

# Create the heatmap
plt.figure(figsize=(12, 8))
sns.heatmap(normalized_df, annot=True, cmap='Blues', linewidths=0.5, fmt=".2f")
plt.title(f'Occurrences of Connectives per 10,000 Tokens, {generation}, {language}')
plt.xlabel('Text Type')
plt.ylabel('Connective')
plt.tight_layout()
plt.show()
