import spacy
import statistics

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

# Define the texts
human_text = " Talk of the NSA 's reported spying on Germany and other allies dominated Merkel 's news conference in Brussels , Belgium . It illustrated the anger over this story in Europe and the challenges facing Washington because of it .   The Chancellor insisted she isn't the only one concerned ; other European leaders , she said , voiced similar sentiments during the first day of the summit Thursday .   Her comments echoed some she'd made upon arriving Thursday in Belgium , when she said that discussions of ' what sort of data protection do we need and what transparency is there ' should now be on European leaders ' agenda .   ' We need trust , ... ' she said . Spying among friends is never acceptable . "

generated_text = "A shift in America's surveillance policy is needed, not just reassurances, she continued. Merkel's clear message echoed across the Atlantic Ocean and left a sobering echo in its wake: trust between the United States and its European allies was severely compromised. The international political climate had taken a chilly turn as details of widespread US spying operations were revealed, with Germany being one among the many aggrieved nations who expressed their grave concerns over privacy breaches conducted by American intelligence. The sense of betrayal was acutely felt. Governments across Europe feared that confidential telephone conversations, strategic deliberations, even private communications had been intercepted by an ostensible ally. Yet Merkel remained firm in her demand for sweeping changes from Washington."

# Function to analyze text
def analyze_text(text, tp):
    # Process the text
    doc = nlp(text)

    # Calculate words per sentence
    sent_lengths = [len(sentence) for sentence in doc.sents]
    avg_words_per_sentence = sum(sent_lengths) / len(sent_lengths)

    # Count long words (> 6 characters)
    long_words = [token.text for token in doc if len(token.text) > 6]

    # Count POS tags
    pos_counts = {
        "NOUN": 0, "VERB": 0, "ADJ": 0, "PROPN": 0, "ADV": 0,
        "PRON": 0, "CCONJ": 0, "SCONJ": 0, "PUNCT": 0
    }
    for token in doc:
        if token.pos_ in pos_counts:
            pos_counts[token.pos_] += 1

    # Calculate POS proportions
    total_words = len(doc)
    pos_proportions = {pos: count / total_words for pos, count in pos_counts.items()}

    # Print results
    print(f"\nAnalysis for {tp} text:")
    print(f"Average words per sentence: {avg_words_per_sentence:.2f}")
    print(f"Number of long words (> 6 characters): {len(long_words)}")
    print("\nPOS counts:")
    for pos, count in pos_counts.items():
        print(f"{pos}: {count}")
    print("\nPOS proportions:")
    for pos, proportion in pos_proportions.items():
        print(f"{pos}: {proportion:.2f}")

# Analyze both texts
analyze_text(human_text, "human")
analyze_text(generated_text, "generated")