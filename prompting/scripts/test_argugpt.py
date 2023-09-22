import requests

API_URL = "https://api-inference.huggingface.co/models/SJTU-CL/RoBERTa-large-ArguGPT"
headers = {"Authorization": "Bearer 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"}
# headers = {"Authorization": f"Bearer {'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'}}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": "Upon further examination, the patient reported experiencing occasional visual disturbances, such as blurred vision and seeing flashing lights, during her headaches. She also mentioned that the headaches tended to occur more frequently during times of stress or lack of sleep. Physical examination revealed no abnormalities, and neurological examination was within normal limits. Given her history of seizures and the presence of visual disturbances, further investigations were warranted to determine the cause of her headaches. An MRI scan of the brain was performed, which revealed characteristic findings consistent with Sturge-Weber syndrome (SWS). The imaging showed leptomeningeal angiomas involving the left cerebral hemisphere, along with cortical atrophy and calcifications. These findings were consistent with the known neurologic manifestations of SWS. The patient was referred to a neurologist specializing in headache disorders for further evaluation and management. The neurologist confirmed the diagnosis of SWS and explained that the headaches experienced by the patient were likely related to the underlying condition. Treatment options were discussed, and a multidisciplinary approach involving neurology, ophthalmology, and dermatology was recommended to address the various aspects of SWS. The patient was prescribed a prophylactic medication to help manage her headaches and was advised to maintain a regular sleep schedule, manage stress levels, and avoid triggers that could exacerbate her symptoms. Regular follow-up appointments were scheduled to monitor the patient's progress and adjust the treatment plan as needed. The patient was also provided with information and resources to help her better understand and cope with the challenges associated with SWS.In conclusion, this 21-year-old female patient with a history of seizures and diagnosed with Sturge-Weber syndrome presented with frequent non-pulsating headaches. The headaches were relieved by non-steroidal anti-inflammatory drugs and were not worsened by physical activity. The presence of visual disturbances during the headaches, along with characteristic findings on brain imaging, confirmed the association between SWS and her headache symptoms. A comprehensive management plan involving multiple specialties was implemented to address the patient's needs and improve her quality of life.",
})

print(output)