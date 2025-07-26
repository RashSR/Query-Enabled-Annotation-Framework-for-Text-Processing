class MessageToken:
    def __init__(self, start_pos: int, end_pos: int, text: str, spacy_match = None, lt_match = None):
        self._start_pos = start_pos
        self._end_pos = end_pos
        self._text = text
        self._spacy_match = spacy_match
        self._lt_match = lt_match
        self._is_flagged = False #If found in a searchresult -> flag it

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
    def lt_match(self):
        return self._lt_match

    @property
    def spacy_match(self):
        return self._spacy_match
    
    @property
    def is_flagged(self):
        return self._is_flagged
    
    def __str__(self):
        return (f"MessageToken(text='{self._text}', "
                f"Index: {self._start_pos} - {self._end_pos},"
                f"lt_match={self._lt_match}, "
                f"spacy_match={self._spacy_match})")
    

    #Do i need to search over more messages? When does one end? After the other person types something?
