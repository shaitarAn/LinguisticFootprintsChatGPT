import os
import openai
import requests
import json
import re
import argparse
from texts import *

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

if corpus == "cnn":
  intext = cnn_news
elif corpus == "e3c":
  intext = e3c_clinical_case
elif corpus == "ggponc":
   intext = ggponc
elif corpus == "pubmed_en":
   intext = pubmed_en


# Open the JSON file in read mode
with open('prompts.json', 'r') as json_file:
    json_data = json.load(json_file)

if not os.path.exists(f"../output/{corpus}"):
  os.makedirs(f"../output/{corpus}")

for task in ["create", "explain", "continue"]:
  print(corpus)
  print(task)
    
  if task == "continue":
     json_data[corpus][task][1]["content"] = json_data[corpus][task][1]["content"].format(intext=intext[0])
     with open(f"../output/{corpus}/human-cont.txt", "w") as f:
        f.write(intext[1])
  else:
     json_data[corpus][task][1]["content"] = json_data[corpus][task][1]["content"].format(intext=" ".join(intext))
     with open(f"../output/{corpus}/human-full.txt", "w") as f:
        f.write(" ".join(intext))

  # print(data[corpus])
  prompt = json_data[corpus][task]
  # print("prompt:", prompt)

  # print(prompt)

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

  if response.status_code == 200:
    result = response.json()
    print("-----------------------------------")
    print(result["choices"][0]["message"]["content"])
    print("-----------------------------------")
    if not os.path.exists(f"../output/{corpus}"):
      os.makedirs(f"../output/{corpus}")
    with open(f"../output/{corpus}/{task}_{data['temperature']}_{data['frequency_penalty']}.txt", "w") as f:
        f.write(result["choices"][0]["message"]["content"])
  else:
    print(response.status_code)
    print(response.json())