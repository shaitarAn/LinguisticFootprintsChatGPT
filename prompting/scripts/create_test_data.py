import pandas as pd

# Define the data for the CSV files
data = {
    "Feature1": [1, 2, 3, 4],
    "Feature2": [6, 7, 8, 9],
    "Feature3": [1, 12, 3, 4],
    "Feature4": [10, 7, 8, 1],
    "Feature5": [4, 2, 3, 2],
}

# Create 5 test DataFrames, one for each CSV file
for i in range(5):
    df = pd.DataFrame(data)
    
    # Assign column names
    df.columns = ["feature", "human", "create", "continue", "explain"]
    
    # Save the DataFrame to a CSV file
    file_name = f"../output/test/test_file_{i+1}.csv"
    df.to_csv(file_name, index=False)

    print(f"Created {file_name}")

print("All test files created.")
