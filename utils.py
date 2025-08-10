import spacy
import language_tool_python
import re
from mainFlask.classes.message import Message
from mainFlask.classes.chat import Chat
from mainFlask.classes.messagetype import MessageType
from datetime import datetime
from mainFlask.classes.ltmatch import LTMatch
from mainFlask.classes.spacymatch import SpacyMatch
from mainFlask.data.cachestore import CacheStore
from itertools import chain
from collections import Counter

#TODO: try nltk also

# Load german spaCy model and initialize language tool -> only loaded once
nlp = spacy.load("de_core_news_lg") #possible values: de_core_news_sm de_core_news_md, de_core_news_lg (more powerful)

#only check for the websever if it will be used
_tool_instance = None
def get_tool():
    global _tool_instance
    if _tool_instance is None:
        _tool_instance = language_tool_python.LanguageTool('de-DE', remote_server='http://localhost:8081')
    return _tool_instance

# Store author_id in the session
def set_active_author(session, author_id):
    session['author_id'] = author_id

# get stored author
def get_active_author(session):
    return CacheStore.Instance().get_author_by_id(session.get('author_id'))

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
            msg.annotated_text = analyze_msg_with_language_tool(msg)
        chat.add_message(msg)
        msg_id = msg_id + 1
    
    return chat

# region Spacy

#https://spacy.io/usage/linguistic-features -> a lot more features to look at
#Possible Output for spacy analyzed texts:
#Text: The original word text.
#Lemma: The base form of the word.
#POS: The simple UPOS part-of-speech tag.
#Tag: The detailed part-of-speech tag.
#Dep: Syntactic dependency, i.e. the relation between tokens. just a big number -> further investigation needed
#Shape: The word shape – capitalization, punctuation, digits. just a big number -> further investigation needed
#is alpha: Is the token an alpha character?
#is stop: Is the token part of a stop list, i.e. the most common words of the language?

#TODO look up lemmatizer
def analyze_msg_with_spacy(msg: Message) -> list[SpacyMatch]:
    #TODO: check for MessageType.TEXT
    doc = nlp(msg.content)

    for token in doc:

        morph = token.morph
        pos = token.pos_

        tense = person = verb_form = voice = mood = None
        degree = gram_case = number = gender = pron_type = None

        #TODO: check if there are more pos than that
        if pos in ("VERB", "AUX"):
            tense = morph.get("Tense")[0] if morph.get("Tense") else None
            person = morph.get("Person")[0] if morph.get("Person") else None
            verb_form = morph.get("VerbForm")[0] if morph.get("VerbForm") else None
            voice = morph.get("Voice")[0] if morph.get("Voice") else None
            mood = morph.get("Mood")[0] if morph.get("Mood") else None

        if pos in ("ADJ", "ADV"):
            degree = morph.get("Degree")[0] if morph.get("Degree") else None

        if pos in ("NOUN", "PROPN", "PRON", "ADJ", "DET"):
            gram_case = morph.get("Case")[0] if morph.get("Case") else None
            number = morph.get("Number")[0] if morph.get("Number") else None
            gender = morph.get("Gender")[0] if morph.get("Gender") else None

        if pos in ("PRON", "DET"):
            pron_type = morph.get("PronType")[0] if morph.get("PronType") else None

        if pos == "NUM":
            number = morph.get("Number")[0] if morph.get("Number") else number
            gram_case = morph.get("Case")[0] if morph.get("Case") else gram_case

        if pos in ("CCONJ", "SCONJ", "PART", "ADP", "INTJ", "X"):
            print(f"[Info] POS {pos} has minimal or no morphological features.")

        if pos in ("PUNCT", "SPACE"):
            print(f"[Skipping] POS {pos} (punctuation or space)")

        spacy_match = SpacyMatch(
            message_id=msg.message_id,
            chat_id=msg.chat_id,
            start_pos=token.idx,
            end_pos=token.idx + len(token),
            text=token.text,
            lemma=token.lemma_,
            pos=token.pos_,
            tag=token.tag_,
            is_alpha=token.is_alpha,
            is_stop=token.is_stop,
            tense=tense,
            person=person,
            verb_form=verb_form,
            voice=voice,
            degree=degree,
            gram_case=gram_case,
            number=number,
            gender=gender,
            mood=mood,
            pron_type=pron_type
        )

        CacheStore.Instance().create_spacy_match(spacy_match)

#annotation code 
        #annotated_text = ""
        #if not token.pos_ == "PUNCT":
            #annotated_text = annotated_text + " "
        #annotated_token = f"<span data-error=\"{token.lemma_}\">{token.text}</span>"
        #annotated_text = annotated_text + annotated_token
# endregion 

# region Language Tool

#TODO: check if it is possible to start with more threads https://stackoverflow.com/questions/72500635/how-to-speed-up-language-tool-python-library-use-case
def analyze_msg_with_language_tool(msg: Message): #TODO: check for MessageType.TEXT

    if(msg is None):
        return None
    
    #only analyse if needed -> TODO needs rework
    if(msg.annotated_text is None or msg.annotated_text == ""):
        text = msg.content

        #check the text
        matches = get_tool().check(text)

        #convert text to a list to change it easily
        text_list = list(text)

        #gather all found errors
        for match in reversed(matches):
            startPos = match.offset
            endPos = match.offset + match.errorLength
            errortext = text[startPos : endPos]
            lt_match = LTMatch(msg.message_id, msg.chat_id, startPos, endPos, errortext, match.category, match.ruleId)
            created_lt_match = CacheStore.Instance().create_lt_match(lt_match)
            msg.add_error(created_lt_match)
            add_error_tags(match.ruleId, errortext, startPos, endPos, text_list)

        modified_text = ''.join(text_list)
        msg.annotated_text = modified_text

# print all usefull error informations
def print_error(match, startPos, endPos, text):
    fehlertext = text[startPos : endPos]
    print(f"Gefundener Fehler: '{fehlertext}'")
    print(f"Nachricht: {match.message}")
    if(len(match.replacements) > 0):
        print(f"Vorschlag: {match.replacements}")
    print(f"Position: {startPos}-{endPos}")
    print(f"Fehlerregel ID: {match.ruleId}")
    print(f"Kategorie: {match.category}")
    print(f"RuleIssueType: {match.ruleIssueType}")

#add html style tags
def add_error_tags(ruleId, fehlertext, startPos, endPos, text_list):
    error_tag = f"<span data-error=\"{ruleId}\">{fehlertext}</span>"
    text_list[startPos : endPos] = list(error_tag)

# endregion

#return a combined list of all messages without duplicates
def or_result_messages(lists: list[list[Message]]) -> list[Message]:
    flat = chain.from_iterable(lists)

    seen_ids = set()
    unique_messages : list[Message] = []
    for msg in flat:
        if msg.message_id not in seen_ids:
            unique_messages.append(msg)
            seen_ids.add(msg.message_id)

    return unique_messages

#return a list with messages that are in every given list
def and_result_messages(lists: list[list[Message]]) -> list[Message]:

    total_lists: int = len(lists)
    key=lambda m: m.message_id

    per_list_keys = ( {key(m) for m in lst} for lst in lists )
    counts = Counter(chain.from_iterable(per_list_keys))
    
    first: list[Message] = lists[0]
    result: list[Message] = [m for m in first if counts[key(m)] == total_lists]

    return result

    
