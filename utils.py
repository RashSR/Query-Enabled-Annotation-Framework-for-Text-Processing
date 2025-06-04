import spacy
import language_tool_python

# Load german spaCy model and initialize language tool -> only loaded once
nlp = spacy.load("de_core_news_lg") #possible values: de_core_news_sm de_core_news_md, de_core_news_lg (more powerful)
tool = language_tool_python.LanguageTool('de-DE', remote_server='http://localhost:8081')

def load_single_chat_from_file(filePath):
    return None


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

# region Spacy

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

#useful to print spacy like annotations
def print_tokennized_word(key, value):
    if (len(value) != 0):
        print(f"{key}: {value}")

# endregion 

# region Language Tool
from classes.message import Message
def anaylze_msg_with_language_tool(msg: Message):
    text = msg.content
    #check the text
    matches = tool.check(text)

    #convert text to a list to change it easily
    text_list = list(text)

    #find all different ruleIds
    found_ruleIds = []

    #print all found errors
    for match in reversed(matches):
        startPos = match.offset
        endPos = match.offset + match.errorLength
        fehlertext = text[startPos : endPos]
        msg.add_to_error_dict(match.category)
        #print_error(match, startPos, endPos, text)
        add_error_tags(match.ruleId, fehlertext, startPos, endPos, text_list)
        if not (found_ruleIds.__contains__((match.ruleId, match.message))):
            found_ruleIds.append((match.ruleId, match.message))
        #print("---")

    # Den bearbeiteten Text ausgeben
    modified_text = ''.join(text_list)
    return modified_text

# print all usefull error informations
def print_error(match, startPos, endPos, text):
    fehlertext = text[startPos : endPos]
    print(f"Gefundener Fehler: '{fehlertext}'")
    print(f"Nachricht: {match.message}")
    if(len(match.replacements) > 0):
        print(f"Vorschlag: {match.replacements}")
    print(f"Position: {startPos}-{endPos}")
    print(convert_message(match.ruleId))
    print(f"Fehlerregel ID: {match.ruleId}")
    print(f"Kategorie: {match.category}")
    print(f"RuleIssueType: {match.ruleIssueType}")

#convert the match.messages in a useful description
def convert_message(lt_message):
    match lt_message:
        case "GERMAN_SPELLER_RULE":
            return "Tippfehler"
        case "PLURAL_APOSTROPH":
            return "falsches Apostroph bei Pluralbildung"
        case "KOMMA_INFINITIVGRUPPEN":
            return "Komma bei Infinitvgruppe"
        case "DE_CASE":
            return "Falsche Großschreibung"
        case "GERMAN_WORD_REPEAT_RULE":
            return "Wortwiederholung"
        case "DE_DOUBLE_PUNCTUATION":
            return "Doppelte Punktuation"
        case "UPPERCASE_SENTENCE_START":
            return "Großschreibung am Satzanfang"   
        case _:
            print("bisher unbekannt")

#add html style tags
def add_error_tags(ruleId, fehlertext, startPos, endPos, text_list):
    error_tag = f"<span data-error=\"{ruleId}\">{fehlertext}</span>"
    text_list[startPos : endPos] = list(error_tag)

# endregion