from classes.message import Message

class SearchResult:
    def __init__(self, message: Message, keyword, matched_word, case_sensitive=False, selected_color = None, left = None, right = None):
        self._message = message
        self.keyword = keyword
        self.matched_word = matched_word
        self.case_sensitive = case_sensitive
        self._selected_color = selected_color
        if(left == None and right == None):
            self._calc_left_and_right()
        else:
            self._left = left
            self._right = right
    
    def _calc_left_and_right(self):
        content = self.message.content
        keyword = self.keyword

        # Case-insensitive match using .lower()
        if not self.case_sensitive:
            content_lower = content.lower()
            keyword_lower = keyword.lower()
            index = content_lower.find(keyword_lower)
        else:
            index = content.find(keyword)

        if index != -1:
            self._left = content[:index]
            self._right = content[index + len(keyword):]
        else:
            self._left = content
            self._right = ''

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

    @property
    def message(self) -> Message:
        return self._message

    @message.setter
    def message(self, value: Message):
        self._message = value

    @property
    def selected_color(self):
        return self._selected_color
    
    @selected_color.setter
    def selected_color(self, value):
        self._selected_color = value

    def __repr__(self):
        return f"search_result(left={self._left!r}, keyword={self.keyword!r}, right={self._right!r})"
    
    def __eq__(self, other):
        if not isinstance(other, SearchResult):
            return NotImplemented
        return (
            self.message == other.message and
            self.keyword == other.keyword and
            self.matched_word == other.matched_word and
            self.case_sensitive == other.case_sensitive
        )

    def __hash__(self):
        return hash((
            self.message,  # Ensure Message is hashable!
            self.keyword,
            self.matched_word,
            self.case_sensitive
        ))