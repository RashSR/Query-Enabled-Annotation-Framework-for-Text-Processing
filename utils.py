import spacy

# Load german spaCy model
nlp = spacy.load("de_core_news_lg") #possible values: de_core_news_sm de_core_news_md, de_core_news_lg (more powerful)

def extract_text_from_html(filePath, withTags=False):
    from bs4 import BeautifulSoup
    with open(filePath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # Find the <body>
    body = soup.body
    # Remove all <script> tags inside <body> and its contents
    for script_tag in body.find_all('script'):
        script_tag.decompose()
    #remove all <span> tags
    if not withTags:
        for span in body.find_all('span'):
            span.unwrap()
    # Get only the inner HTML (without <body> tags)
    inner_html = body.decode_contents()
    return inner_html

#useful to print spacy like annotations
def print_tokennized_word(key, value):
    if (len(value) != 0):
        print(f"{key}: {value}")

def analyze_msg_with_spacy(text):
    doc = nlp(text)
    annotated_text = ""

    # priniting information
    for token in doc:
        print(f"Wort: {token.text}") #
        if not token.pos_ == "PUNCT":
            annotated_text = annotated_text + " "
        annotated_token = f"<span data-error=\"{token.lemma_}\">{token.text}</span>"
        annotated_text = annotated_text + annotated_token
        print(f"Grundform: {token.lemma_}") #Grundform
        print(f"POS-Tag: {token.pos_}") #Wortart
        if token.pos_ == "VERB":
            print_tokennized_word("Tempus", token.morph.get('Tense')) #Zeitform
            print_tokennized_word("Person", token.morph.get('Person')) #Person des Verbs
            print_tokennized_word("VerbForm", token.morph.get('VerbForm')) #Verbform finites Verb, Partizip
            print_tokennized_word("Stimme", token.morph.get('Voice')) #Aktiv oder Passiv #Aktiv oder Passiv
        if token.pos_ == "ADJ" or token.pos_ == "ADV":
            print_tokennized_word("Grad", token.morph.get('Degree')) #Grad der Steigerung
        print_tokennized_word("Kasus", token.morph.get('Case')) #Kasus/"Fall"
        print_tokennized_word("Zahl", token.morph.get('Number')) #Singular/Plural
        print_tokennized_word("Geschlecht", token.morph.get('Gender')) #Geschlecht Fem/Masc
        print_tokennized_word("Modus", token.morph.get('Mood')) #Indikativ/Konjunktiv

        print("---")