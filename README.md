# Tracing Linguistic Footprints of ChatGPT Across Tasks, Domains, and Personas

## Brief Description

This repository contains the code and data supporting the research paper "Tracing Linguistic Footprints of ChatGPT Across Tasks, Domains and Personas in English and German." The project explores how the output of large language models like ChatGPT differs from human-generated text and analyzes the impact of task-specific prompting on linguistic features in both English and German texts.

## Usage

### Text generation 

`cd text_generation`

The script `generate.py` sends requests to the OpenAI-API. As input it takes a JSON file in the following form:
```json
{
  "file1": {
    "title": "very interesting and engaging topic",
    "prompt": "part of the text to use for the prompt",
    "text": "the rest of the text"
  },
  "file2": {
    
  }
}
```
The `make_json.py` script can be used to create such a file from a collection of txt files (see below). 
From the input for every file in the JSON the API is called to generate a text of more than 500 tokens.
After making sure that both the remainder of the human text (without the pompt) and the machine generated text are of the same length
by truncating the shorter one, it saves them in two separate folders called `human` and `machine`.  An example call looks like this:

`generate.py gpt-3.5-turbo path_to_input_file.json de`

In this example the model gpt-3.5-turbo is used. Additional positional arguments are the path to the input and the language of the document (needed for the tokenizer).
This will create an output folder in the directory from which the script is run with two subfolders `human` and `machine`. Optionally the output directory can be specified
with the flag `--outfolder`, for more info on the optional arguments see `generate.py --help`.

**Generate personas**:

`bash call_generate_personas.sh`
  - **Parameters**: 
    - model: `gpt-4`, `gpt-3.5-turbo-16k`
    - outfolder: `../generated_data` in this folder subfolders task/corpus/system will be created
    - infolder: `../data_collection/100_files_json/` all the JSON for generation
  - **Calls python script**: `generate_personas.py`
  - **Output file structure**: `f"{outputdir}/{corpus}/{task}/{file_counter}.txt"`

`prompts.json` contains all the prompts and personas

### Feature extraction

`cd feature_extraction/scripts/`

Update the lists of corpora, domains, and tasks in the `config.py`.

Specify your input data and output directories in `bash run_experiments.sh`, which executes two bash scripts:

  - `bash run_extract_BiasMT_features.sh` extracts metrics for Sophistication, Lexical and Morphological richness using the [BiasMT tool](https://github.com/dimitarsh1/BiasMT/).

  - `bash run_extract_other_features.sh` extracts other features using the [TextDescriptives library](https://hlasse.github.io/TextDescriptives/descriptivestats.html), also reorganizes results, and transforms dataframes for further analysis.

`features_list.py` contains several dictionnaries with feature names:

- features_list is a list of TextDescriptives features
- features_custom is a list of custom-added feature names
- features_to_visualize_dict is a dictionnary with feature names used by textDescriptives and throughout the project as keys and modified feature names as values
- features_raw_counts is a list of features that are measured in raw counts

### Analysis 

`cd analysis/scripts/`

`bash run_analysis.sh`
  - **Parameters**:
    - alpha: `0.01`, `0.05`
    - method: `bon` (bonferroni), `bh` (benjamini-hochberg)

## Cite this paper (to be updated)

```
@article{YourLastName2024,
  title={Tracing Linguistic Footprints of ChatGPT Across Tasks, Domains and Personas in English and German},
  author={Anastassia Shaitarova, Nikolaj Bauer, Jannis Vamvas, Martin Volk},
  journal={Journal Name},
  year={2024},
  volume={xx},
  pages={xxx-xxx}
}
```




