from enum import Enum

class FilterType(Enum):
    NOT = "NOT"
    AND = "AND"
    OR = "OR"
    OBJECT = "OBJECT"