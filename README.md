# Tracing Linguistic Footprints of ChatGPT Across Tasks, Domains, and Personas

## Brief Description

This repository contains the code and data supporting the research paper "Tracing Linguistic Footprints of ChatGPT Across Tasks, Domains and Personas in English and German." The project explores how the output of large language models like ChatGPT differs from human-generated text and analyzes the impact of task-specific prompting on linguistic features in both English and German texts.

The code is generalizable to include any number of corpora, domains, and tasks by simply updating `config/config.yaml`

## Usage

### Text generation 

- `cd text_generation`

- Set up your OpenAI API key: `export OPENAI_API_KEY="your_openai_api_key_here"`

- Update prompts, tasks, and personas in `prompts.json` (also, see `prompts_ashuman_asmachine.json`)

- Create an input JSON file for each corpus. See `make_json.py` for an example. The JSON file format should be as follows:
  ```json
  {
    "human_file1": {
      "title": "very interesting and engaging topic",
      "prompt": "part of the text to use for the prompt",
      "text": "the rest of the text"
    },
    "human_file2": {
      
    }
  }
  ```

- `bash call_generate_personas.sh`
  - model: `gpt-4` specify you rOpenAI model
  - infolder: `../data_collection/100_files_json/` human texts for prompting and analysis
  - outfolder: `../generated_data` see the resulting directory tree representation below 
  - config: `../config/config.yaml`
  - calls  `generate_personas.py`
  
  ```
  generated_data/
  ├── corpus1/
  │   ├── task1/
  │   │   ├── human/
  │   │   │   ├── 0.txt
  │   │   │   ├── 1.txt
  │   │   │   └── ...
  │   │   └── system1/
  │   │       ├── 0.txt
  │   │       ├── 1.txt
  │   │       └── ...
  │   └── task2/
  │       ├── human/
  │       │   ├── 0.txt
  │       │   ├── 1.txt
  │       │   └── ...
  │       └── system1/
  │           ├── 0.txt
  │           ├── 1.txt
  │           └── ...
  └── corpus2/
      ├── task1/
      │   ├── human/
  ```

### Feature extraction

`cd feature_extraction/scripts/`

Specify your input data and output directories in `bash run_experiments.sh`, which executes two bash scripts:

  - `bash run_extract_BiasMT_features.sh` extracts metrics for Sophistication, Lexical and Morphological richness using the [BiasMT tool](https://github.com/dimitarsh1/BiasMT/).

  - `bash run_extract_other_features.sh`:
    - extracts features using the [TextDescriptives library](https://hlasse.github.io/TextDescriptives/descriptivestats.html)
    - extracts connectives
    - uses custom formula for German Flesch Reading Ease
    - reorganizes results and transforms dataframes for further analysis

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




