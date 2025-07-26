class MessageToken:
    def __init__(self, start_pos: int, end_pos: int, text: str):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._text = text
        self._lt_matches = []
        self._spacy_matches = []

    @property
    def start_pos(self):
        return self._start_pos
    
    @property
    def end_pos(self):
        return self._end_pos

    @property
    def text(self):
        return self._text

    @property
    def lt_matches(self):
        return self._lt_matches

    @property
    def spacy_matches(self):
        return self._spacy_matches
    
    def __str__(self):
        return (f"MessageToken(text='{self._text}', "
                f"Index: {self._start_pos} - {self._end_pos}"
                f"lt_matches={len(self._lt_matches)}, "
                f"spacy_matches={len(self._spacy_matches)})")