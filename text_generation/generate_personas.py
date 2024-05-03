import os
import openai
import requests
import json
import re
import argparse
import backoff
<<<<<<< HEAD
=======
from texts import *
>>>>>>> 3fcef2ca (viz for paper)
import time
from generate import OpenAiModels

# ############################################

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG")

# ############################################

parser = argparse.ArgumentParser()
# parser.add_argument("prompt", type=str, help="Prompt to use for text generation")
parser.add_argument("model", type=str, choices=["gpt-3.5-turbo", "gpt-3.5-turbo-16k", "gpt-4"], help="OpenAI model to use")
parser.add_argument("--temperature", "-t", type=float, required=False, default=1, help="Temperature to use for text generation")
parser.add_argument("--frequency_penalty", "-fp", type=float, required=False, default=1, help="Frequency penalty to use for text generation")
parser.add_argument("--corpus", "-c", type=str, required=True, help="Corpus name to use for text generation")
# add inputdir and outputdir
parser.add_argument("--inputdir", "-i", type=str, required=True, help="Input directory")
parser.add_argument("--outputdir", "-o", type=str, required=True, help="Output directory")
parser.add_argument("--min_len", type=int, default=500, help="minimum length of the generated texts")

args = parser.parse_args()

# ############################################

# Replace {intext} with an actual value
intext = ""

corpus = args.corpus
model_name = args.model
inputdir = args.inputdir
outputdir = args.outputdir
temperature = args.temperature
frequency_penalty = args.frequency_penalty
min_len = args.min_len

# ############################################

model = OpenAiModels(model_name, openai.api_key, openai.organization)

@backoff.on_exception(backoff.expo, openai.APIError)
@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def call_openai(prompt):
  
  # at ther time, I am not keeping track of tokens per second
  tokens_per_second, new_text = model.generate(prompt, temperature, frequency_penalty)

  return tokens_per_second, new_text

# ############################################

# human texts directory path
human_texts = os.path.expanduser(inputdir)

# JSON file with prompts and personas
with open('prompts.json', 'r') as json_file:
    json_prompts = json.load(json_file)

if not os.path.exists(f"{outputdir}/{corpus}"):
  os.makedirs(f"{outputdir}/{corpus}")

if not os.path.exists(f"{outputdir}/{corpus}/human"):
    os.makedirs(f"{outputdir}/{corpus}/human")

# ############################################
  
file_counter = 0

# iterate over human files
with open(f"{human_texts}{corpus}.json", 'r') as f:
    json_texts = json.load(f)

    for file in json_texts:
      file_counter += 1
      print(file)

      title = json_texts[file]["title"] + json_texts[file]["prompt"]
      title = re.sub(r"\n", " ", title)
      
      main_text = json_texts[file]["text"]
      main_text = re.sub(r"\n", " ", main_text)
      if len(main_text.split(" ")) > 1500:
        main_text = " ".join(main_text.split(" ")[:1500])

      # ############################################

      for task in ["continue", "create", "explain"]:
        
        if not os.path.exists(f"{outputdir}/{corpus}/{task}"):
          os.makedirs(f"{outputdir}/{corpus}/{task}")

        json_prompt_before_intext = json_prompts[corpus][task][1]["content"].split(" {intext}")[0]
        json_prompt_after_intext = json_prompts[corpus][task][1]["content"].split(" {intext}")[1]
        # print(json_prompt_before_intext)
           
        if task == "explain":
          user_content = json_prompts[corpus][task][1]["content"].format(intext=main_text)

        else:
          user_content = json_prompts[corpus][task][1]["content"].format(intext=title)
        
        with open(f"{outputdir}/{corpus}/human/{file_counter}.txt", "w") as f:
             f.write(main_text)

        system_content = json_prompts[corpus][task][0]["content"]
        continue_content = json_prompts[corpus][task][2]["content"]

        # ############################################

        prompt =[ {
          "role": "system",
          "content": system_content
        },{
          "role": "user",
          "content": user_content
        }]

        # ############################################

        tokens_per_second, gen_text = call_openai(prompt)

        # ############################################
        # remove prompt text, if it was repeated
        gen_text = gen_text.replace(system_content, "")
        gen_text = gen_text.replace(json_prompt_before_intext, "") 
        gen_text = gen_text.replace(json_prompt_after_intext, "") 
        num_toks = len(gen_text.split())

        # ############################################

        # add text until long enough
        while num_toks < min_len:
            print("not long enough, generating more")
            # print(continue_content)

            new_prompt_text = ""

            # feed only the last 300 tokens back into the model 
            if len(gen_text.split()) > 300:
              new_prompt_text = " ".join(gen_text.split()[-300:])
              print("cut the prompt")
              print(new_prompt_text)
              print()
            else:
               new_prompt_text = gen_text

            # ############################################
               
            prompt =[ {
              "role": "system",
              "content": system_content
            },{
              "role": "user",
              "content": " ".join([new_prompt_text, continue_content])
            }]

            # ############################################

            # generate again
            _, new_text = call_openai(prompt)

            # ############################################
            # check if the prompt is included (unlikely, but better save than sorry)
            new_text = new_text.replace(system_content, "")
            new_text = new_text.replace(json_prompt_before_intext, "") 
            new_text = new_text.replace(json_prompt_after_intext, "")
            
            # save the full text that was generated so far
            # check if the model put the beginning from the prompt into the text
            if gen_text in new_text:
                gen_text = new_text
            else:
                gen_text += " " + new_text
            num_toks = len(gen_text.split())

        # ############################################
        with open(f"{outputdir}/{corpus}/{task}/{file_counter}.txt", "w") as f:
            f.write(gen_text)
