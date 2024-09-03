import os
import re
import langdetect

data_dir = "../../data_2407_gpt4o/ggponc"

# Define the word to search for
word = "Darüber hinaus"

# Initialize the dictionary to store occurrences
word_dict = {}
languages = []

# Iterate over all tasks (subdirectories) in the data directory
for task in os.listdir(data_dir):
    task_dir = os.path.join(data_dir, task)
    if os.path.isdir(task_dir):  # Check if it's a directory
        for file in os.listdir(task_dir):
            filename = file.split(".")[0]  # Remove file extension
            file_path = os.path.join(task_dir, file)
            with open(file_path, "r") as f:
                text = f.readlines()
                # Check if the text is in German
                try:
                    lang = langdetect.detect("".join(text))
                except langdetect.lang_detect_exception.LangDetectException:
                    lang = None
                languages.append(lang)
                if lang != "de":
                    print(f"File {file_path} is not in German") 

                # Initialize the count for this file
                file_count = 0
                # Count the number of occurrences of the word in each line of the text
                for i, line in enumerate(text):
                    count = len(re.findall(r'\b' + re.escape(word) + r'\b', line))
                    file_count += count

                if task not in word_dict:
                    word_dict[task] = {}  # Initialize the nested dictionary for the task
                word_dict[task][filename] = file_count  # Store the count for this file


print(set(languages))
# # Print the resulting dictionary
# for task, files in word_dict.items():
#     print(f"Task: {task}")
#     for filename, count in files.items():
#         print(f"  File: {filename}, Count: {count}")
#     print()
