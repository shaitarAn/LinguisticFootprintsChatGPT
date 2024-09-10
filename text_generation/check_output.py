from generate import *
import os
import argparse
import json
import re
from helper import parse_filename
from tqdm import tqdm


def repetition(text:str):
    first_words, rest = " ".join(text.split()[:20]), " ".join(text.split()[20:])
    if first_words in rest:
        return True




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infolder", help="folder in which to check the generated files and replace them. "
                                         "It should be the top folder under which the domains with both human and machine files are"
                                         " (e.g. final_files_simple_prompt")
    parser.add_argument("junkfolder", help="folder in which to store the faulty files. A subfolder with the domain name will be created")
    parser.add_argument("domain", choices=["20min", "cnn", "e3c", "GGPONC", "pubmed_de", "pubmed_en", "zora_de", "zora_en", "cs_en", "cs_de"])
    parser.add_argument("lang", choices=["de", "en"])
    parser.add_argument("--prompt_file", type=str, default="", help="File containing the prompt. The prompt can include placeholders"
                                                        "<title> and <prompt> for including text from the human files.")
    parser.add_argument("--json", default=r"../data/sample_100_json",
                        help="Folder with the JSON files (if a text needs to be recreated)."
                             " Default is ../data/sample_100_json")
    parser.add_argument("--model_name", default="gpt-3.5-turbo", choices=["gpt-3.5-turbo"])
    args = parser.parse_args()
    infolder = args.infolder
    junkfolder = args.junkfolder
    domain = args.domain
    lang = args.lang
    prompt_file = args.prompt_file
    json_path = args.json
    model_name = args.model_name

    # get the source_dict for regeneration
    with open(os.path.join(json_path, f"{domain}.json"), "r", encoding="utf-8") as injson:
        source_dict = json.load(injson)

    # define the directories
    machine_folder = os.path.join(infolder, domain, "machine")
    human_folder = os.path.join(infolder, domain, "human")
    domain_folder = os.path.join(infolder, domain)
    junkfolder = os.path.join(junkfolder, domain)

    if not os.path.exists(junkfolder):
        os.mkdir(junkfolder)

    # Initialize a tokenizer with the specified language
    tokenizer = Tokenizer(lang)

    filepaths = [os.path.join(machine_folder, filename) for filename in os.listdir(machine_folder)]

    count = 0
    for filepath in tqdm(filepaths):
        with open(filepath, "r", encoding="utf-8") as infile:
            text = infile.read()


        if repetition(text):

            count += 1


            # initialize model for regeneration:
            api_key = os.getenv("OPENAI_KEY")
            org_id = os.getenv("ORG_ID")
            model = OpenAiModels(model_name, api_key, org_id)

            # Initialize a tokenizer with the specified language
            tokenizer = Tokenizer(lang)

            # get the prompt template
            prompt_source = get_prompt(lang, prompt_file)

            # finding the old filename (before the truncation, to access the dictionary
            filename = os.path.basename(filepath)
            year, title, _, lang = parse_filename(filename)
            if domain == "GGPONC":  # no year in GGPONC
                pattern = rf"{re.escape(title)}_\d+_{lang}"
            else:
                pattern = rf"{year}-{re.escape(title)}_\d+_{lang}"
            possible_matches = [filename for filename in source_dict.keys() if re.match(pattern, filename)]
            if len(possible_matches) == 1:
                old_filename = possible_matches[0]
            else:
                print("Ambiguous Filename!!!")
                print(filename, possible_matches)
                exit(1)

            # Initialize the specified model for generation
            api_key = os.getenv("OPENAI_KEY")
            org_id = os.getenv("ORG_ID")
            model = OpenAiModels(model_name, api_key, org_id)

            # regenerate the text
            i = 1
            print(f"\nrewriting file '{filename}'. Iterations: {i}")
            machine, human, new_filename = get_formatted_texts(old_filename, source_dict, prompt_source, model, tokenizer)

            # in case the first conversion has not worked...
            while repetition(machine):
                i += 1
                print(f"\nrewriting file '{filename}'. Iterations: {i}")
                machine, human, new_filename = get_formatted_texts(old_filename, source_dict, prompt_source, model, tokenizer)


            # move the repetitive file to another folder
            os.rename(os.path.join(machine_folder, filename), os.path.join(junkfolder, filename))

            # Remove the human file, we have to retruncate the original text
            os.remove(os.path.join(human_folder, filename))

            # write new files
            write_texts(machine, human, new_filename, domain_folder)
            print(f"{filename} rewritten after {i} iteration(s)\n")


    print(f"\n{count} files were rewritten")



