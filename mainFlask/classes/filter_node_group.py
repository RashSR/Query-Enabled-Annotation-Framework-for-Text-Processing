from enum import Enum

class FilterNodeGroup(Enum):
    WORD = "word"
    RULE_ID = "error-ruleId"
    CATEGORY = "error-category"
    AUTHOR = "author"
    RECIPIENT = "recipient"
    #EMOJI = "emoji"
    LEMMA = "lemma"
    WORTART = "pos"
    #FEINTAG = "feintag"
    #BUCHSTABEN = "nurbuchstaben" -> isAlpha
    #FUNKTIONSWORT = "funktionswort"
    TEMPUS = "tense"
    PERSON = "person"
    VERBFORM = "verb_form"
    STIMME = "voice"
    STEIGERUNGSGRAD = "degree"
    KASUS = "gram_case"
    NUMERUS = "number" #singular/plural
    GENUS = "gender"
    MOUDS = "mood"
    PRONOMENTYP = "pron_type"
    TAG = "tag"

    @classmethod
    def is_spacy_filter_group(cls, filter_node_group):
        SPACY_FILTER_GROUPS = {
            FilterNodeGroup.WORTART,
            FilterNodeGroup.LEMMA,
            FilterNodeGroup.PRONOMENTYP,
            FilterNodeGroup.TEMPUS,
            FilterNodeGroup.PERSON,
            FilterNodeGroup.VERBFORM,
            FilterNodeGroup.STIMME,
            FilterNodeGroup.STEIGERUNGSGRAD,
            FilterNodeGroup.KASUS,
            FilterNodeGroup.NUMERUS,
            FilterNodeGroup.GENUS,
            FilterNodeGroup.MOUDS,
            FilterNodeGroup.TAG,
        }
        return filter_node_group in SPACY_FILTER_GROUPS

    