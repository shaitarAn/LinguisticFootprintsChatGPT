import os

# Specify the directory path
directory_path = os.path.expanduser("~/switchdrive/IMAGINE_files/chatGPT/project_2/final_files_simple_prompt/GGPONC/machine/")

# List all files in the directory
files = os.listdir(directory_path)

# Loop through the files and rename them
for filename in files:
    if " " in filename:
        new_filename = filename.replace(" ", "_")
        old_path = os.path.join(directory_path, filename)
        new_path = os.path.join(directory_path, new_filename)
        os.rename(old_path, new_path)
