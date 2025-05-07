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

# print all usefull error informations
def print_error(match, startPos, endPos):
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

#add html style tags
def add_error_tags(ruleId, fehlertext, startPos, endPos):
    error_tag = f"<span data-error=\"{ruleId}\">{fehlertext}</span>"
    text_list[startPos : endPos] = list(error_tag)

#useful to print spacy like annotations
def print_tokennized_word(key, value):
    if (len(value) != 0):
        print(f"{key}: {value}")


import language_tool_python

tool = language_tool_python.LanguageTool('de-DE', remote_server='http://localhost:8081')

#load text from a txt file
with open('texts\longer_text.txt', 'r', encoding='utf-8') as file:
    text = file.read()

print("Originaltext:")
print(text)
print("\n")

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
    print_error(match, startPos, endPos)
    add_error_tags(match.ruleId, fehlertext, startPos, endPos)
    if not (found_ruleIds.__contains__((match.ruleId, match.message))):
        found_ruleIds.append((match.ruleId, match.message))
    print("---")

# Den bearbeiteten Text ausgeben
modified_text = ''.join(text_list)

print("\nBearbeiteter Text:")
print(modified_text)

# Read the template file
with open("misc/template.html", "r", encoding="utf-8") as f:
    template = f.read()

# Replace placeholders
filled_html = template.replace("{{analyzedText}}", modified_text)

# Write to output file
with open("output.html", "w", encoding="utf-8") as f:
    f.write(filled_html)

print("Generated 'output.html' successfully.")



print(f"Anzahl gefundener Fehler: {len(matches)}")
print(f"Anzahl gefundener Fehlerarten: {len(found_ruleIds)}")

for element in found_ruleIds:
    print(f"ID: {element[0]}, Message: {element[1]}")

#TODO: if only one replacement is possible -> show it
    
import spacy

# Load german spaCy model
nlp = spacy.load("de_core_news_sm") #also possible: de_core_news_md, de_core_news_lg (more powerful)

# Beispieltext
text = "Der kleine Hund läuft schnell durch den Park. Gestern hatte er einen großen Streit mit einem anderen Hund, aber er ist jetzt wieder friedlich. Der Hund wird oft von seinem Besitzer geführt, der immer freundlich ist. Sie haben ihre Route durch den Park geändert, weil sie den großen Baum, den sie immer bewunderten, gesehen haben. Manchmal kommt der Hund auch an den Teich, um die Enten zu sehen. "

doc = nlp(text)

# priniting information
for token in doc:
    print(f"Wort: {token.text}") #
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

#possible values for tempus: 
#-Präsens (Pres): "Ich gehe", "Ich habe".
#-Präteritum (Past): "Ich ging", "Ich hatte".
#-Perfekt (Perf): "Ich bin gegangen", "Ich habe gegessen".
#-Futur I (Fut): "Ich werde gehen".
#-Futur II (Fut2): "Ich werde gegangen sein".

