import csv
import json

# Load the JSON data from your file
with open('prompts.json', 'r') as json_file:
    data = json.load(json_file)

# Open a CSV file for writing
with open('prompts.csv', 'w', newline='') as csv_file:
    # Extract the keys for column headers
    columns = ['corpus']
    for task, items in data['zora_en'].items():
        for idx, item in enumerate(items):
            if item['role'] == 'system':
                columns.append(f'{task}_persona')
            elif item['role'] == 'user':
                columns.append(f'{task}_{idx}')
            print(columns)

    writer = csv.DictWriter(csv_file, fieldnames=columns)
    
    # Write the header row
    writer.writeheader()

    # Write the data
    for corpus, tasks in data.items():
        row = {'corpus': corpus}
        for task, items in tasks.items():
            for idx, item in enumerate(items):
                if item['role'] == 'system':
                    row[f'{task}_persona'] = item['content']
                elif item['role'] == 'user':
                    row[f'{task}_{idx}'] = item["content"]
        writer.writerow(row)
