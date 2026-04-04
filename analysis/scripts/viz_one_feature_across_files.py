import pandas as pd
import matplotlib.pyplot as plt

features = ["pos_prop_CCONJ", "first_order_coherence"]
            # "dependency_distance_mean", "prop_adjacent_dependency_relation_mean", "first_order_coherence", "second_order_coherence"]

for f in features:

    # feature = f"../../feature_extraction/results/per_language/english/{f}.csv"
    # feature_other_lang = f"../../feature_extraction/results/per_language/german/{f}.csv"
    feature_other_lang = f"../../feature_extraction/2403gpt4/results/per_feature/{f}/20min.csv"

    # dfe = pd.read_csv(feature)
    df = pd.read_csv(feature_other_lang)

    # Step 2: Plot the data
    plt.figure(figsize=(10, 6))

    # Plot each column as a line
    plt.plot(df.index, df['human'], label='Human', marker='o')
    plt.plot(df.index, df['continue'], label='Continue', marker='o')
    plt.plot(df.index, df['explain'], label='Explain', marker='o')
    plt.plot(df.index, df['create'], label='Create', marker='o')

    # Step 3: Customize the plot
    plt.title('Comparison of Text Lengths Across 100 Rows')
    plt.xlabel('Row Index')
    plt.ylabel('Values')
    plt.legend(title='System', loc='best')
    plt.grid(True)

    # Display the plot
    plt.show()

