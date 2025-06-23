class SearchResult:
    def __init__(self, message, keyword, left = None, right = None):
        self.message = message
        self.keyword = keyword
        if(left == None and right == None):
            self._calc_left_and_right(message, keyword)
        else:
            self._left = left
            self._right = right

    def __repr__(self):
        return f"search_result(left={self._left!r}, keyword={self.keyword!r}, right={self._right!r})"
    
    #at this point we know that the keyword is in the message
    def _calc_left_and_right(self, message, keyword):
        parts = message.content.split(keyword, 1)
        self._left = parts[0]
        self._right = parts[1]

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, value):
        self._left = value

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = value
