from enum import Enum

class FilterMode(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    OBJECT = "OBJECT"