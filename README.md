# prompts_n_coherence


## text generation
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
