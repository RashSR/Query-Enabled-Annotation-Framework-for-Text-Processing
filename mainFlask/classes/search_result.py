from .message import Message
import re

class SearchResult:
    def __init__(
        self, 
        message: Message, 
        keyword, 
        matched_word, 
        case_sensitive=False, 
        selected_color=None, 
        left=None, 
        right=None,
        match_index=0,
        start_pos=None,
        end_pos=None
    ):
        self._message = message
        self.keyword = keyword
        self.matched_word = matched_word
        self.case_sensitive = case_sensitive
        self._selected_color = selected_color
        self.match_index = match_index
        self.start_pos = start_pos
        self.end_pos = end_pos

        if left is None and right is None:
            self._calc_left_and_right()
        else:
            self._left = left
            self._right = right

    def _calc_left_and_right(self):
        content = self.message.content

        # If manual start/end positions are provided, use them directly
        if self.start_pos is not None and self.end_pos is not None:
            self._left = content[:self.start_pos]
            self._right = content[self.end_pos:]
            return

        # Otherwise, do keyword search
        keyword = self.keyword
        content_to_search = content if self.case_sensitive else content.lower()
        keyword_to_find = keyword if self.case_sensitive else keyword.lower()

        matches = [m for m in re.finditer(re.escape(keyword_to_find), content_to_search)]

        if self.match_index < len(matches):
            match = matches[self.match_index]
            self.start_pos = match.start()
            self.end_pos = match.end()
            self._left = content[:self.start_pos]
            self._right = content[self.end_pos:]
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
            self.case_sensitive == other.case_sensitive and
            self.match_index == other.match_index and
            self.start_pos == other.start_pos and
            self.end_pos == other.end_pos
        )

    def __hash__(self):
        return hash((
            self.message,
            self.keyword,
            self.matched_word,
            self.case_sensitive,
            self.match_index,
            self.start_pos,
            self.end_pos
        ))
