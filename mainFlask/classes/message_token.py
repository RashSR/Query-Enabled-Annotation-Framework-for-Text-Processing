from .annotation import Annotation
from .ltmatch import LTMatch
from .spacymatch import SpacyMatch

class MessageToken:
    def __init__(self, start_pos: int, end_pos: int, text: str, spacy_match = None, lt_matches = [], annotations = []):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._text = text
        self._spacy_match = spacy_match
        self._lt_matches = lt_matches
        self._annotations = annotations
        self._is_flagged: bool = False #If found in a searchresult -> flag it

    @property
    def start_pos(self) -> int:
        return self._start_pos
    
    @property
    def end_pos(self) -> int:
        return self._end_pos

    @property
    def text(self) -> str:
        return self._text

    @property
    def lt_matches(self) -> list[LTMatch]:
        return self._lt_matches

    @property
    def spacy_match(self) -> SpacyMatch:
        return self._spacy_match
    
    @property
    def annotations(self) -> list[Annotation]:
        return self._annotations
    
    @property
    def is_flagged(self) -> bool:
        return self._is_flagged
    
    @is_flagged.setter
    def is_flagged(self, value: bool):
        self._is_flagged = value

    def __str__(self):
        return (f"MessageToken(text='{self._text}', "
                f"Index: {self._start_pos} - {self._end_pos}, "
                f"is_flagged: {self.is_flagged}, "
                f"annotations={len(self._annotations)}, "
                f"lt_matches={len(self._lt_matches)}, "
                f"spacy_match={self._spacy_match})")

