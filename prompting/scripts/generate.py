import os
import openai
import requests
import json
from texts import *

openai.organization = "org-HjWBseLU0iDzg4cx01nO6JrY"
openai.api_key = "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"


intext = pubmed_en # e3c_clinical_case, cnn_news, pubmed_en, ggponc

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {openai.api_key}'
  }

data = {
  'model': 'gpt-3.5-turbo',
  'messages':[
    {
      "role": "system",
      "content": "You are an academic, writing a new article for publication."
      },
      {
        "role": "user",
        "content": f"Read the provided title: {intext[0]} and the abstarct: {intext[1]}. Write an entirely new introduction section for your academic paper, using the title and abstract as a guide."
    }
  ],
  "max_tokens":1000,
  "top_p":1,
  "frequency_penalty":0,
  "presence_penalty":0,
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

if response.status_code == 200:
  result = response.json()
  print(result["choices"][0]["message"]["content"])
else:
  print(response.status_code)
  print(response.json())
