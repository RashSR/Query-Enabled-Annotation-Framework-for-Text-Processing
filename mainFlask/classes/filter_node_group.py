from enum import Enum

class FilterNodeGroup(Enum):
    WORD = "word"
    RULE_ID = "error-ruleId"
    CATEGORY = "error-category"
    AUTHOR = "author"
    EMOJI = "emoji"