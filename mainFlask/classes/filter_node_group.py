from enum import Enum

class FilterNodeGroup(Enum):
    WORD = "word"
    RULE_ID = "error-ruleId"
    CATEGORY = "error-category"
    AUTHOR = "author"
    RECIPIENT = "recipient"
    #EMOJI = "emoji"
    LEMMA = "grundform"
    WORTART = "wortart"
    #FEINTAG = "feintag"
    #BUCHSTABEN = "nurbuchstaben" -> isAlpha
    #FUNKTIONSWORT = "funktionswort"
    TEMPUS = "tempus"
    PERSON = "person"
    VERBFORM = "verform"
    STIMME = "stimme"
    STEIGERUNGSGRAD = "steigerungsgrad"
    KASUS = "kasus"
    NUMERUS = "numerus" #singular/plural
    GENUS = "gender"
    MOUDS = "modus"
    PRONOMENTYP = "pronomentyp"

    