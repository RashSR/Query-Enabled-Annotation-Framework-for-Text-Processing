import spacy
import language_tool_python
import re
from classes.message import Message
from classes.chat import Chat
from classes.messagetype import MessageType
from datetime import datetime

#TODO: try nltk also

# Load german spaCy model and initialize language tool -> only loaded once
nlp = spacy.load("de_core_news_lg") #possible values: de_core_news_sm de_core_news_md, de_core_news_lg (more powerful)
tool = language_tool_python.LanguageTool('de-DE', remote_server='http://localhost:8081')

def load_all_chats_from_files(ids, isAnalyzing = False):
    chats = []
    for i in ids:
        chat = load_single_chat_from_file(i, isAnalyzing)
        chats.append(chat)

    return chats

def print_progress_bar(iteration, total, length=40):
    percent = (iteration / total)
    filled_length = int(length * percent)
    bar = '█' * filled_length + '-' * (length - filled_length)
    print(f'\rProcessing |{bar}| {percent*100:.1f}% complete', end='')

def load_single_chat_from_file(id, isAnalyzing = False) -> Chat:
    filename = "whatsapp_chat_"

    # Read the file
    with open("texts/" + filename + str(id) + ".txt", "r", encoding="utf-8") as file:
        chat_text = file.read()

    # Pattern to match each message
    pattern = r'\[(\d{1,2}:\d{2}), (\d{1,2}\.\d{1,2}\.\d{4})\] ([^:]+): (.*?)((?=\n\[\d{1,2}:\d{2}, \d{1,2}\.\d{1,2}\.\d{4}\])|$)'

    # Find all matches
    matches = re.findall(pattern, chat_text, re.DOTALL)

    chat = Chat(id)
    msg_id = 0

    total = len(matches)
    # Iterate each message
    for time, date, sender, message, _ in matches:
        print_progress_bar(msg_id + 1, total)
        str_date = date + " " + time
        date_obj = datetime.strptime(str_date, "%d.%m.%Y %H:%M")
        msg = Message(id, msg_id, sender, date_obj, message.strip())
        if isAnalyzing and msg.message_type == MessageType.TEXT:
            #analyze_msg_with_spacy(msg.content)
            msg.annotated_text = anaylze_msg_with_language_tool(msg)
        chat.add_message(msg)
        msg_id = msg_id + 1
    
    return chat

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
def anaylze_msg_with_language_tool(msg: Message):

    if(msg is None):
        return None
    
    if(msg.annotated_text is None or msg.annotated_text == ""):
        text = msg.content

        #check the text
        matches = tool.check(text)

        #convert text to a list to change it easily
        text_list = list(text)

        #find all different ruleIds
        found_ruleIds = []

        #gather all found errors
        for match in reversed(matches):
            startPos = match.offset
            endPos = match.offset + match.errorLength
            fehlertext = text[startPos : endPos]
            msg.add_to_error_dict(match.category)
            add_error_tags(match.ruleId, fehlertext, startPos, endPos, text_list)
            if not (found_ruleIds.__contains__((match.ruleId, match.message))):
                found_ruleIds.append((match.ruleId, match.message))

        modified_text = ''.join(text_list)
        msg.annotated_text = modified_text
    
    return msg.annotated_text

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