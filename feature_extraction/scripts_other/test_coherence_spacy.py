import spacy
import textdescriptives as td
nlp = spacy.load("en_core_web_lg")
nlp.add_pipe("textdescriptives/coherence")
text_machine = "This clinical case involves a 21-year-old female patient who has been diagnosed with Sturge-Weber Syndrome (SWS). SWS is a rare disorder characterized by abnormal blood vessels affecting the skin, eyes, and brain. In this case, the patient has a port wine birthmark (facial nevus) on her right forehead, eyelid, nasal wing, and cheek, which is a common feature of SWS. The patient has been experiencing frequent headaches for two years. These headaches are non-pulsating, bilateral (both sides of the head), pressing in quality, and last for hours. However, the headaches are relieved by non-steroidal anti-inflammatory drugs (NSAIDs) and are not worsened by physical activity. The absence of nausea, aura, and a negative family history of headache suggest that these headaches may be related to SWS rather than a primary headache disorder. The patient also has a history of seizures that began in the fifteenth day of her life. These seizures were characterized by tonic-clonic contractions and led to her diagnosis of SWS. At the age of 6, she underwent a procedure called callosotomy to control her seizures. However, at the age of 18, she had another seizure during a laser treatment for her port wine birthmark. Since then, she has been prescribed carbamazepine, an anti-seizure medication, and has not had any seizures. In terms of her physical examination, the patient has a right-sided overgrowth of the gingiva (the gums) that is bright red in color and shows blanching upon pressure. This suggests an angiomatous enlargement of the blood vessels in the gingiva, which is another common manifestation of SWS. Additionally, there is mild asymmetry in her extremities, with her left arm and leg being slightly smaller and exhibiting hemiparesis (weakness or paralysis on one side of the body). On ophthalmological evaluation, glaucoma (increased pressure within the eye) was diagnosed in her right eye. Neuroimaging studies, including cranial CT scans and Gadolinium-enhanced brain MRI, revealed various abnormalities in the patient's brain. These include diffuse atrophy (shrinkage) on the right hemisphere, irregular double-contoured gyriform cortical calcifications (calcium deposits in the brain) in the right occipital area, and multiple dilated pial venous vascular structures on the right hemisphere. The asymmetry of the right calvarial thickness (thickness of the skull) and the smaller size of the right hemisphere compared to the left are also observed. Furthermore, the T2-weighted MRI shows extensive venous formations around the corpus of the right lateral ventricle, at Gallen vein localization, at the perivascular space anterior to the third ventricle at Willis polygon localization, and at the right temporooccipital area at quadrigeminal cistern localization. These findings further support the presence of abnormal blood vessels in the brain associated with SWS.Psychiatric examination reveals signs of an anxiety disorder in the patient, for which she is prescribed ketiapin and venlafaxine. She is also prescribed NSAID drugs for her headaches. After a week of treatment, her headaches showed slight improvement in terms of heaviness, but the frequency remained the same. In terms of her cognitive assessment, the patient underwent a Proteus intelligence test, which revealed a score of 75 points, indicating mild mental retardation. In summary, this clinical case involves a young female patient with Sturge-Weber Syndrome, characterized by a port wine birthmark, seizures, extensive brain abnormalities, glaucoma, hemiparesis, gingival overgrowth, and headaches. The patient also presents with signs of an anxiety disorder and mild mental retardation. Treatment with anti-seizure medication and medications for anxiety and headaches has been initiated, but the headaches have not significantly improved."

text_human = "A 21 year old female patient with the diagnosis of SWS suffering from headaches admitted to our clinic. She had a 2 year history of frequent non-pulsating headaches. Her headache was relieving with non-steroidal anti-inflammatory drugs and was not worsening with physical activity. There was no nausea or aura like symptoms accompanying the headache. Headaches were lasting for hours. The pain was bilateral, generalized and pressing in quality. The family history for headache was negative. She had a history of seizures occurring in the fifteenth day of life described as attacks of tonic clonic contractions and that's when she was diagnosed with SWS. At the age of 6 she had a history of callosotomy to control her seizures. At the age of 18 during a laser treatment done in order to get rid of her port wine birthmark she had her first seizure since callosotomy. After that she was prescribed carbamazepine 400 mg at daily dose and never had a seizure since then. According to the story taken from her parents even though she had a normal development at infancy she barely graduated from elementary school and she's hardly literate. There was nothing significant on her family history except for her elder sister's port wine stain on her face. The elder sister had no feature of SWS and no researches were done regarding her stain. She was inscribed daily doses of ketiapin 25 mg for anxiety disorder and venlafaxine 75 mg for both anxiety disorder and the chronic headaches. She was also inscribed NSAID drugs. After the first week of this treatment her headaches were slightly decreased by heaviness but the frequency was the same. At her physical examination a facial nevus -occurred due to choroid angioma-on the right forehead, right eyelid, nasal wing and the cheek was observed. Intra oral examination showed a right sided overgrowth of gingiva. Gingival overgrowth was bright red in color and showed blanching on applying pressure suggesting angiomatous enlargement. On her extremities a mild asymmetry was visible. Her left arm and leg was slightly smaller in portions and showed hemiparesis both in the upper and lower extremities of the same size. On her ophthalmological evaluation she was diagnosed with glaucoma of the right eye. On her psychiatric examination she showed signs of anxiety disorder. Her neurological examination was not remarkable except for her hemiparesis. Cranial CT scans showed diffuse atrophy in the right hemisphere and irregular double-contoured gyriform cortical calcifications in the right occipital area. Gadolinium enhanced brain MRI revealed multiple dilated pial venous vascular structures on right hemisphere also with the diffuse atrophy on the same side. Axial T1 weighted cranial MRI shows right calvarial thickness compared to the left and right hemisphere is asymmetrically smaller than the left. In addition to that, T2 weighted MRI shows extensive venous formations around corpus of right lateral ventricle and at Gallen vein localization and widespread vascular formations are seen at perivascular space, anterior to third ventricle at Willis polygon localization and at right temporooccipital area at quadrigeminal cistern localization. She was performed a proteus intelligence test in which she had 75 points and accepted as mildly mentally retarded. Proteus intelligence test in which she had 75 points and accepted as mildly mentally retarded."

doc = nlp(text_human)

for token in doc:
    if token.is_oov:
        print(token.text, token.has_vector, token.vector_norm, token.is_oov)

# all attributes are stored as a dict in the ._.coherence attribute
doc._.coherence

# first and second order coherence values are also added as separate attributes
# note that the first/first two sentences do not have any values for first/second order
# coherence, respectively, as they require 1 or 2 sentences to average over
doc._.first_order_coherence_values
doc._.second_order_coherence_values

# extract to dataframe
td.extract_df(doc)

# print the doc with the coherence values
print(doc._.coherence)