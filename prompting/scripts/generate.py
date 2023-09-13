import os
import openai
import requests
import json

openai.organization = "org-HjWBseLU0iDzg4cx01nO6JrY"
openai.api_key = "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"

intext = "A 21 year old female patient with the diagnosis of SWS suffering from headaches admitted to our clinic. She had a 2 year history of frequent non-pulsating headaches. Her headache was relieving with non-steroidal anti-inflammatory drugs and was not worsening with physical activity. There was no nausea or aura like symptoms accompanying the headache. Headaches were lasting for hours. The pain was bilateral, generalized and pressing in quality. The family history for headache was negative. She had a history of seizures occurring in the fifteenth day of life described as attacks of tonic clonic contractions and that's when she was diagnosed with SWS. At the age of 6 she had a history of callosotomy to control her seizures. At the age of 18 during a laser treatment done in order to get rid of her port wine birthmark she had her first seizure since callosotomy. After that she was prescribed carbamazepine 400 mg at daily dose and never had a seizure since then. According to the story taken from her parents even though she had a normal development at infancy she barely graduated from elementary school and she's hardly literate. There was nothing significant on her family history except for her elder sister's port wine stain on her face. The elder sister had no feature of SWS and no researches were done regarding her stain. She was inscribed daily doses of ketiapin 25 mg for anxiety disorder and venlafaxine 75 mg for both anxiety disorder and the chronic headaches. She was also inscribed NSAID drugs. After the first week of this treatment her headaches were slightly decreased by heaviness but the frequency was the same. At her physical examination a facial nevus -occurred due to choroid angioma-on the right forehead, right eyelid, nasal wing and the cheek was observed. Intra oral examination showed a right sided overgrowth of gingiva. Gingival overgrowth was bright red in color and showed blanching on applying pressure suggesting angiomatous enlargement. On her extremities a mild asymmetry was visible. Her left arm and leg was slightly smaller in portions and showed hemiparesis both in the upper and lower extremities of the same size. On her ophthalmological evaluation she was diagnosed with glaucoma of the right eye. On her psychiatric examination she showed signs of anxiety disorder. Her neurological examination was not remarkable except for her hemiparesis. Cranial CT scans showed diffuse atrophy in the right hemisphere and irregular double-contoured gyriform cortical calcifications in the right occipital area. Gadolinium enhanced brain MRI revealed multiple dilated pial venous vascular structures on right hemisphere also with the diffuse atrophy on the same side. Axial T1 weighted cranial MRI shows right calvarial thickness compared to the left and right hemisphere is asymmetrically smaller than the left. In addition to that, T2 weighted MRI shows extensive venous formations around corpus of right lateral ventricle and at Gallen vein localization and widespread vascular formations are seen at perivascular space, anterior to third ventricle at Willis polygon localization and at right temporooccipital area at quadrigeminal cistern localization. She was performed a proteus intelligence test in which she had 75 points and accepted as mildly mentally retarded. Proteus intelligence test in which she had 75 points and accepted as mildly mentally retarded."

prompt = command+intext

headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Bearer {openai.api_key}'
  }

data = {
  'model': 'gpt-3.5-turbo',
  'messages':[
    {
      "role": "system",
      "content": "You are a nurse who is writing an imaginary clinical case, using a real clinical case as an example."
      },
      {
        "role": "user",
      "content": f"Use this clinical case as an example: {intext}. Imagine a patient with a similar condition. Write a clinical case about this patient. Match the length and the writing style of the example case."
    }
  ],
  # "max_tokens":4095,
  "top_p":1,
  "frequency_penalty":0,
  "presence_penalty":0,
}

response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers,data=json.dumps(data))

if response.status_code == 200:
  result = response.json()
  # print(result)
  # print("------------------")
  print(result["choices"][0]["message"]["content"])
else:
  print(response.status_code)
  print(response.json())
# output = openai.Completion.create(
#   model="gpt-3.5-turbo",
#   prompt=command+intext,
#   max_tokens=600,
#   temperature=0.7,
#   top_p=1,
#   n=1,
#   stream=False,
#   logprobs=None
#   # stop="\n"
# )

# print(output["choices"][0]["text"].strip())
# print(output)
