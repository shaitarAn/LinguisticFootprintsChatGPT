import os
import requests
import openai
import json
import re
from helper import Tokenizer, parse_filename
import argparse
from tqdm import tqdm
from datetime import datetime
import time
import copy
print (os.environ.keys())



class OpenAiModels:

    def __init__(self, model_name:str, api_key, org_id=None):
        self.api_key = api_key
        self.model_name = model_name

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        if org_id:
            self.headers["OpenAI-Organization"] = org_id


    def generate(self, messages, temp, freq_pen):
        """returns completion time in tokens per second and the generated text"""
        # todo: test the 16k model
        if not self.model_name in ["gpt-3.5-turbo", "gpt-3.5-turbo-16k"]:
            print(f"{self.model_name} not implemented")
            exit(1)

        data = {
            'model': self.model_name,
            'messages': messages,
            'temperature': temp,
            'frequency_penalty': freq_pen,

            # todo: we could do this also variable, from calling the script, and with defaults, as with temp
            # just in case you want to change it later?
            'presence_penalty': 0,
            'max_tokens': 2000
        }

        for i in range(10):
            time_0 = time.perf_counter()
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=self.headers, data=json.dumps(data))
            time_1 = time.perf_counter()
            if response.status_code == 200:
                result = response.json()

                if not "error" in result:
                    completion_tokens = result["usage"]["completion_tokens"]
                    tokens_per_second = completion_tokens/(time_1-time_0)
                    # todo: add checkpoint if the prompt is in the generated text and if so, run again
                    # I think this is happening in function generate()
                    return tokens_per_second, result["choices"][0]["message"]["content"]  # result["choices"][0]["text"]
                else:
                    print("\n\nOpenAI error: ", result["error"])

            elif response.status_code < 500:
                print("\n\nHTTP ERROR HERE:", response.status_code)
                print(self.api_key)

                if response.status_code == 400:
                    print(f"\nPrompt:\n{messages}\n############################\n")

                try:
                    error_dict = response.json()
                    print(error_dict)
                except:
                    pass
                exit()


            else:  # Serverside errors (<500)
                time.sleep(1.2 ** i)  # exponential increase between failed requests, last request waits for approx. 5 seconds

        print("##########\nGeneration failed")
        print("\n\nHTTP ERROR:", response.status_code)
        try:
            print(f"Reason: {response.reason}")
        except:
            pass
        exit()


# Todo: here go without it, and then make a separate script, that truncates all 4 versions to the same length
# def truncate_texts(machine_text, human_text, tokenizer):
#
#     machine_text_tok_list = tokenizer.token_list(machine_text)
#     human_text_tok_list = tokenizer.token_list(human_text)
#
#     min_length = min(len(machine_text_tok_list), len(human_text_tok_list))
#
#     return " ".join(machine_text_tok_list[:min_length]), " ".join(human_text_tok_list[:min_length]), min_length

# todo: rewrite to work with new prompting system
def generate(model, prompt_template, prompt_text, temp, freq_pen, min_len=500):
    """Generates a text using the model and given parameters.
    Asks for more if the min_len is not reached
    @:return tokens_per_second [float]: estimated generations speed in tokens per second
    @:return text[str]: generated text, untokenized"""

    # create messages from the template, i.e. start conversation
    intext = " ".join(prompt_text.split()[:1000])  # truncate it if too long
    prompt_filled = copy.deepcopy(prompt_template)
    prompt_filled[1]["content"] = prompt_filled[1]["content"].format(intext=intext)  # fill in the text where needed
    messages = prompt_filled[:2]

    # print(messages)

    # generate a first time, save tokens per second
    tokens_per_second, new_text = model.generate(messages, temp, freq_pen)
    gen_text = new_text.replace(prompt_text, "")  # remove prompt text, if it was repeated
    num_toks = len(gen_text.split())

    # add text until long enough
    while num_toks < min_len:
        print("not long enough, generating more")
        # add the assistant response to the messages, always redo, so we have a max of 3 conversation inputs
        # [{role: "system", content: "Your are this and that"},
        # {role:"user", content: "initial prompt"},
        # {role:"system", content: "so far generated text"},
        # {role: "user", content: "additional prompt"}]
        messages = prompt_filled[:2]
        # add the so far generated text
        messages.append({
            "role": "assistant", "content": gen_text
        })
        # add the additional prompt:
        messages.append(prompt_template[2])

        # generate again
        _, new_text = model.generate(messages, temp, freq_pen)
        # check if the prompt is included (unlikely, but better save than sorry)
        new_text = new_text.replace(prompt_text, "")
        # save the full text that was generated so far
        # check if the model put the beginning from the prompt into the text
        if gen_text in new_text:
            gen_text = new_text
        else:
            gen_text += " " + new_text
        num_toks = len(gen_text.split())

    return tokens_per_second, gen_text

def update_num_toks_in_filename(text, filename):
    """naive estimate of the number of tokens for the new filename"""
    year, title, _, lang = parse_filename(filename)
    num_toks = len(text.split())
    if year:
        new_filename = f"{year}-{title}_{num_toks}_{lang}.txt"
    else:  # The GGPONC corpus has no years,
        new_filename = f"{title}_{num_toks}_{lang}.txt"
    return new_filename

# todo: new folder structure, machine has additional subfolders "continue, explain and create"
# def write_texts(machine, human, outfolder, prompt_type, filename):
#     """ write the two text file in two folders "machine" and "human"""
#     outfolders = [f"{outfolder}/machine/{prompt_type}", f"{outfolder}/human"]
#     for text, folder in zip([machine, human], outfolders):
#         if not os.path.exists(folder):
#             os.makedirs(folder)
#         new_filename = update_num_toks_in_filename(text, filename)
#         filepath = f"{folder}/{new_filename}"
#         with open(filepath, "w", encoding="utf-8") as outfile:
#             outfile.write(text)

def write_text(text, filename, outfolder, prompt_type):
    """write the generated text"""
    filepath = os.path.join(outfolder, "machine", prompt_type, filename)
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(text)

# todo: Rewrite to make it take the prompts.json as input
# Arguments should be corpus:str, type:str (!! find better variable name, it should be "continue, explain, create"
# additionalprompt=False In case it is asking form more text.
# def get_prompt(prompt_template, text, messages=[]):
#     """returns the list of messages that are to be sent to the api"""
#
#     if not messages:  # add the system description and the first message
#         # fill in the text where needed, truncate it if too long
#         intext = " ".join(text.split()[:1000])
#         prompt_template[1]["content"].format(intext=intext)
#         messages += prompt_template[:2]
#     else:  # just add the auxiliary prompt to the conversation
#         messages.append(prompt_template[2])
#
#     return messages
    # """Returns the prompt, either from a file, or creates the simple prompt"""
    # if prompt_file:
    #     with open(prompt_file, "r", encoding="utf-8") as infile:
    #         prompt_source = infile.read()
    # else:
    #     if lang == "en":
    #         prompt_source = "Complete the following text:\n<title>\n\n<prompt>"
    #     if lang == "de":
    #         prompt_source = "Vervollständige den folgenden text:\n<title>\n\n<prompt>"
    #
    # return prompt_source


def generate_from_filename(filename, file_counter):
    """function to generate from a single file
    to use in a for-loop or on a single file below"""
    global temp
    global freq_pen
    global source_dict
    global model
    global prompt_template
    global time_log
    global min_len
    global corpus

    # define the prompt text:
    if prompt_type == "continue" or prompt_type == "create":
        prompt_text = f"{source_dict[filename]['title']}\n\n{source_dict[filename]['prompt']}"
    else:
        prompt_text = f"{source_dict[filename]['text']}"


    tokens_per_second, machine_text = generate(model, prompt_template, prompt_text, temp, freq_pen, min_len)
    if time_log:
        with open(completion_filepath, "a", encoding="utf-8") as outfile:
            outfile.write(f"{tokens_per_second},{prompt_type},{datetime.now().strftime('%H-%M-%S')}\n")

    # save the generated text in the appropriate folder
    new_filename = update_num_toks_in_filename(machine_text, filename)
    folder = os.path.join(outfolder, corpus, "machine")
    if not os.path.exists(folder):
        os.makedirs(folder)
    filepath = os.path.join(folder, file_counter)
    with open(filepath, "w", encoding="utf-8") as outfile:
        outfile.write(machine_text)

    folder_human = os.path.join(outfolder, corpus, "human")
    if not os.path.exists(folder_human):
        os.makedirs(folder_human)
    with open(os.path.join(folder_human, file_counter), "w") as f:
              f.write(source_dict[filename]['text'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate with the OpenAI API. The API key needs to be specified as an environment variable called 'OPENAI_KEY'"
                                                 "If needed the organization's ID needs to be specified as 'OPENAI_ORG'")
    parser.add_argument("model", type=str, choices=["gpt-3.5-turbo", "gpt-3.5-turbo-16k"], help="OpenAI model to use")
    parser.add_argument("source_file", type=str, help="Filepath of the JSON file with the human texts in following format:"
                                                        "{filename:{'title': '...', 'prompt': '...', 'text': '...'}}")
    parser.add_argument("corpus", type=str, choices=["20min", "cnn", "cs_en", "cs_de", "e3c", "ggponc", "pubmed_de", "pubmed_en", "zora_de", "zora_en"])

    parser.add_argument("--prompt_file", type=str, default="", help="Json file containing the prompts. If it is not given a default 'continue-prompt' will be used.")
    parser.add_argument("--prompt_type", type=str, choices=["continue", "explain", "create"], default="continue")
    parser.add_argument("--outfolder", type=str, default="", help="In this directory a subdirectory for the corpus (if it does not yet exist), will be created "
                                                                  "Then it will create a further subidectory called 'machine' ")
    parser.add_argument("--start_from", type=int, default=0, help="If part of the files are already done, this is the one to start from")
    parser.add_argument("--time_log", type=str, default="", help="create a csv file to save the completion time."
                                                                "Provide the folder in which to save the file here")
    parser.add_argument("--one_file", default="", type=str, help="generate just one file. "
                                                     "provide the filename that will be found in the json_file")
    parser.add_argument("--temp", type=int, default=1, help="Temperature parameter for GPT")
    parser.add_argument("--freq_pen", type=int, default=1, help="Frequency penalty, parameter for GPT")
    parser.add_argument("--min_len", type=int, default=500, help="minimum length of the generated texts")

    args = parser.parse_args()


    model_name = args.model
    source_file = args.source_file
    corpus = args.corpus
    prompt_type = args.prompt_type
    prompt_file = args.prompt_file
    outfolder = args.outfolder
    start_from = args.start_from
    time_log = args.time_log
    one_file = args.one_file
    temp = args.temp
    freq_pen = args.freq_pen
    min_len = args.min_len

    # infer lang from corpus
    corpora_de = ["20min", "cs_de", "ggponc", "pubmed_de", "zora_de"]
    lang = "de" if corpus in corpora_de else "en"

    count_files = 0

    # open the specified source file
    with open(source_file, "r", encoding="utf-8") as infile:
        source_dict = json.load(infile)

    # Open the prompt file, if specified, otherwise apply a simple prompt
    if prompt_file:
        with open(prompt_file, "r", encoding="utf-8") as infile:
            prompt_dict = json.load(infile)
    else:  # default version of the prompt (simple continue)

        prompt_dict = {
            f"{corpus}":{
                f"{prompt_type}": [
                    {
                      "role": "system",
                      "content": ""
                    },
                    {
                      "role": "user",
                      "content": "Continue the following text: {intext}" if lang == "en" else "Vervollständige den folgenden text: {intext}"
                    },
                    {
                      "role": "user",
                      "content": "Continue generating the text" if lang == "en" else "Fahre mit der Erstellung des Textes fort."
                    }
                  ],
            }
        }

    prompt_template = prompt_dict[corpus][prompt_type]

    # Initialize the specified model
    openai.api_key = os.getenv("OPENAI_KEY")
    openai.organization = os.getenv("OPENAI_ORG")

    print("openai.api_key", openai.api_key)
    model = OpenAiModels(model_name, openai.api_key, openai.organization)

    # Initialize a tokenizer with the specified language
    tokenizer = Tokenizer(lang)

    # make default output directory
    if not outfolder:
        outfolder = "output" + datetime.now().strftime("%Y-%m-%d")


    # todo: count generated / billed tokens
    # record completion time

    if args.time_log:
        completion_filename = corpus + datetime.now().strftime("%Y-%m-%d") + ".csv"
        completion_filepath = os.path.join(time_log, completion_filename)
        if not os.path.exists(time_log):
            os.makedirs(time_log)
        # create the new file, if it exists already (i.e. we have generated some texts earlier today) it will just append
        if not os.path.exists(completion_filepath):
            with open(completion_filepath, "w", encoding="utf-8") as outfile:
                outfile.write("Completion-time,prompt-type,time of the call in H-M-S\n")

    if args.one_file:

        generate_from_filename(one_file, count_files)
    else:
        # Go over all the documents
        for filename in tqdm(list(source_dict.keys())[start_from:]):
            count_files += 1
            generate_from_filename(filename, str(count_files))


