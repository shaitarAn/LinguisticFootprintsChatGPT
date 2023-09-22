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
      print(file)

      title_prompt_prompt = json_texts[file]["title"] + json_texts[file]["prompt"]
      title_prompt_prompt = re.sub(r"\n", " ", title_prompt_prompt)
      
      text_prompt = json_texts[file]["text"]
      text_prompt = re.sub(r"\n", " ", text_prompt)
      if len(text_prompt.split(" ")) > 1500:
        text_prompt = " ".join(text_prompt.split(" ")[:1500])

      for task in ["continue", "create", "explain"]:
        print(task)
           
        if task == "explain":
          user_content = json_prompts[corpus][task][1]["content"].format(intext=text_prompt)

        else:
          user_content = json_prompts[corpus][task][1]["content"].format(intext=title_prompt_prompt)
        
        with open(f"../output/{corpus}/human_file{file_counter}.txt", "w") as f:
             f.write(text_prompt)

        system_content = json_prompts[corpus][task][0]["content"]

        prompt =[ {
          "role": "system",
          "content": system_content
        },{
          "role": "user",
          "content": user_content
        }]

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {openai.api_key}'
          }

        data = {
          'model': 'gpt-3.5-turbo-16k',
          'messages':prompt,
          "max_tokens":2000,
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
