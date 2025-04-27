print("------------------- PySpellChecker -----------------------")

from spellchecker import SpellChecker

spell = SpellChecker(language='de')

# Text, den du prüfen möchtest
text = "Hier ist ein Beispeiltext mit Fehern."

# Wort für Wort überprüfen
misspelled = spell.unknown(text.split())

for word in misspelled:
    print(f"Fehlerhaftes Wort: {word}")
    # Vorschläge für die richtige Schreibweise
    print(f"Vorschläge: {spell.candidates(word)}")

print("------------------- TextBlob -----------------------")

from textblob import TextBlob

# Erstelle ein TextBlob-Objekt
text = "Ich habe ein Fehler gemacht."

blob = TextBlob(text)

# Rechtschreibkorrektur
corrected_text = blob.correct()

print(f"Korrigierter Text: {corrected_text}")

print("------------------- Spacy + Spacy-Spellcheck -----------------------")

import spacy
from spacy_langdetect import LanguageDetector
from spacy.language import Language

# Lade das spaCy-Modell (z.B. für Deutsch)
nlp = spacy.load('de_core_news_sm')

# Füge den LanguageDetector zu spaCy hinzu
@Language.component("language_detector")
def language_detector(doc):
    # Benutze die __call__ Methode des LanguageDetector-Objekts
    return LanguageDetector()(doc)

# Füge den LanguageDetector zu der Pipeline hinzu
nlp.add_pipe("language_detector", last=True)

# Beispieltext
text = "Dies ist ein Beispieltext."

# Verarbeite den Text mit spaCy
doc = nlp(text)

# Ausgabe der erkannten Sprache
print(f"Erkannte Sprache: {doc._.language}")



import spacy
from spellchecker import SpellChecker

# Lade das spaCy Modell
nlp = spacy.load('de_core_news_sm')

# Beispieltext
text = "Dies ist ein Beispeiltext mit ein paar Fehlen."

# Verarbeite den Text mit spaCy
doc = nlp(text)

# Rechtschreibprüfung mit pyspellchecker
spell = SpellChecker(language='de')

# Finde falsch geschriebene Wörter
misspelled_words = spell.unknown([token.text for token in doc if token.is_alpha])

print("Falsch geschriebene Wörter:", misspelled_words)

#import spacy
#import language_tool_python

# Lade spaCy Modell
#nlp = spacy.load('de_core_news_sm')

# Beispieltext
#text = "Dies ist ein Beispeiltext mit ein paar Fehlen."

# LanguageTool für die Rechtschreib- und Grammatikprüfung
#tool = language_tool_python.LanguageTool('de-DE') #zertifikat verify='C:/Users/vector_user/Vector_Root_CA_2.0.crt'

# Überprüfe den Text auf Fehler
#matches = tool.check(text)

# Ausgabe der gefundenen Fehler
#for match in matches:
#    print(f"Fehler: {match.message}")
#    print(f"Stellen: {match.context}")






