import os
import openai
import requests
import json
import re
import argparse
from texts import *
import time

openai.organization = "org-HjWBseLU0iDzg4cx01nO6JrY"
openai.api_key = "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"


parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("--temperature", "-t", type=float, required=True, help="Temperature to use for text generation")
parser.add_argument("--frequency_penalty", "-fp", type=float, required=True, help="Frequency penalty to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")

args = parser.parse_args()

# Replace {intext} with an actual value
intext = ""

corpus = args.corpus

class OpenAiModels:

    def __init__(self):

        self.headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {openai.api_key}'
          }

    def generate(self, prompt):
        """returns completion time in tokens per second and the generated text"""

        data = {
          'model': 'gpt-3.5-turbo',
          'messages':prompt,
          "max_tokens":1000,
          "temperature":args.temperature,
          "frequency_penalty":args.frequency_penalty,
          "presence_penalty":0,
        }

        for i in range(10):
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=self.headers, data=json.dumps(data))

            if response.status_code == 200:
                result = response.json()

                if not "error" in result:
                    return result["choices"][0]["message"]["content"]  # result["choices"][0]["text"]
                else:
                    print("\n\nOpenAI error: ", result["error"])

            elif response.status_code < 500:
                print("\n\nHTTP ERROR:", response.status_code)

                if response.status_code == 400:
                    print(f"\nPrompt:\n{prompt}\n############################\n")

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

def generate(model, prompt, min_len = 500):
    
    text = model.generate(prompt)
    num_toks = len(text.split(" "))

    while num_toks < min_len:


        prompt += text
        text += model.generate(prompt)[1]
        num_toks = len(text.split(" "))

    # print("", end="\r\r")
    return text

json_path = os.path.expanduser("~/switchdrive/IMAGINE_files/chatGPT/project_2/5_files_json/")

# Open the JSON file in read mode
with open('prompts.json', 'r') as json_file:
    json_prompts = json.load(json_file)

if not os.path.exists(f"../output/{corpus}"):
  os.makedirs(f"../output/{corpus}")

file_counter = 0

# open jason file whose name contains the corpus name
with open(f"{json_path}{corpus}.json", 'r') as f:
    json_texts = json.load(f)

    for file in json_texts:
      file_counter += 1
      # print(file_counter)
      print(file)
      # print(corpus, json_texts[file]["title"])
      continue_prompt = json_texts[file]["title"] + json_texts[file]["prompt"]
      full_prompt = json_texts[file]["title"] + json_texts[file]["prompt"] + json_texts[file]["text"]
      # replace all newlines with spaces
      continue_prompt = re.sub(r"\n", " ", continue_prompt)
      full_prompt = re.sub(r"\n", " ", full_prompt)
      full_prompt_tokens = full_prompt.split(" ")
      if len(full_prompt_tokens) > 1000:
        full_prompt = " ".join(full_prompt_tokens[:1000])
      # print(continue_prompt)
      # print("--------------------------------------------------")


      for task in ["continue", "create", "explain"]:
        print(task)
           
        if task == "continue":
          user_content = json_prompts[corpus][task][1]["content"].format(intext=continue_prompt)
          with open(f"../output/{corpus}/human-cont_file{file_counter}.txt", "w") as f:
             f.write(json_texts[file]["text"])
        else:
          user_content = json_prompts[corpus][task][1]["content"].format(intext=full_prompt)
          with open(f"../output/{corpus}/human-full_file{file_counter}.txt", "w") as f:
             f.write(full_prompt)

        system_content = json_prompts[corpus][task][0]["content"]

        prompt =[ {
          "role": "system",
          "content": system_content
        },{
          "role": "user",
          "content": user_content
        }]

        # print(prompt)
        # print("--------------------------------------------------")

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {openai.api_key}'
          }

        data = {
          'model': 'gpt-3.5-turbo',
          'messages':prompt,
          "max_tokens":1000,
          "temperature":args.temperature,
          "frequency_penalty":args.frequency_penalty,
          "presence_penalty":0,
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

        # check 
        if response.status_code == 200:
          result = response.json()

          # print("-----------------------------------")
          # print(result["choices"][0]["message"]["content"])
          # print("-----------------------------------")

          if not os.path.exists(f"../output/{corpus}"):
            os.makedirs(f"../output/{corpus}")
          with open(f"../output/{corpus}/{task}_file{file_counter}_{data['temperature']}_{data['frequency_penalty']}.txt", "w") as f:
              f.write(result["choices"][0]["message"]["content"])
        else:
          print(response.status_code)
          print(response.json())


  # model = OpenAiModels()
  # result = generate(model, prompt)
  # print(result)