from myflask.mainFlask.filter_type import FilterType
from classes.message import Message
from classes.author import Author
from myflask.mainFlask.search_result import SearchResult
import re

class FilterNodeObejct:
    def __init__(self, filter_type: FilterType, searchbar_input, selected_value: str, case_sensitive = False, whole_word = False, use_regex = False):
        self._filter_type = filter_type
        self._searchbar_input = searchbar_input
        self._selected_value = selected_value #rigt_side
        self._case_sensitive = case_sensitive
        self._whole_word = whole_word
        self._use_regex = use_regex
        self._result_messages = []
        self._search_result_list = []
        self._selected_color = None

    @property
    def filter_type(self):
        return self._filter_type
    
    @filter_type.setter
    def filter_type(self, value: str):
        self._filter_type = value

    @property
    def searchbar_input(self):
        return self._searchbar_input
    
    @searchbar_input.setter
    def searchbar_input(self, value: str):
        self._searchbar_input = value

    @property
    def selected_value(self):
        return self._selected_value
    
    @selected_value.setter
    def selected_value(self, value):
        self._selected_value = value

    @property
    def case_sensitive(self) -> bool:
        return self._case_sensitive

    @case_sensitive.setter
    def case_sensitive(self, value: bool) -> None:
        self._case_sensitive = bool(value)

    @property
    def whole_word(self) -> bool:
        return self._whole_word

    @whole_word.setter
    def whole_word(self, value: bool) -> None:
        self._whole_word = bool(value)

    @property
    def use_regex(self) -> bool:
        return self._use_regex

    @use_regex.setter
    def use_regex(self, value: bool) -> None:
        self._use_regex = bool(value)

    @property
    def result_messages(self) -> list[Message]:
        return self._result_messages
    
    @result_messages.setter
    def result_messages(self, value: list[Message]):
        self._result_messages = value

    @property
    def search_result_list(self):
        return self._search_result_list
    
    @search_result_list.setter
    def search_result_list(self, value: list[SearchResult]):
        self._search_result_list = value

    @property
    def selected_color(self):
        return self._selected_color
    
    @selected_color.setter
    def selected_color(self, value):
        self._selected_color = value

    def __str__(self):
        toString = f"""left side: {self._filter_type}
        searchbar: {self._searchbar_input}
        selected value: {self._selected_value}
        case_sensitive: {self._case_sensitive}
        whole word: {self._whole_word}
        use regex: {self._use_regex}
        """

        return toString

    def get_result(self, author: Author) -> list[SearchResult]:
        match self._filter_type:
            case FilterType.WORD:
                for msg in author.get_all_own_messages():
                    original_content = msg.content
                    content = original_content if self._case_sensitive else original_content.lower()
                    query = self._searchbar_input if self._case_sensitive else self._searchbar_input.lower()

                    matches = []

                    if self._use_regex:
                        try:
                            pattern = re.compile(query) if self._case_sensitive else re.compile(query, re.IGNORECASE)
                            matches = pattern.finditer(original_content)
                        except re.error:
                            pass  # optionally handle error
                    elif self._whole_word:
                        flags = 0 if self._case_sensitive else re.IGNORECASE
                        pattern = re.compile(r'\b{}\b'.format(re.escape(query)), flags)
                        matches = pattern.finditer(original_content)
                    else:
                        # Not regex, not whole word: simple substring
                        index = content.find(query)
                        if index != -1:
                            matches = [re.Match]  # dummy placeholder
                            matched_word = original_content[index:index+len(self._searchbar_input)]
                            self._search_result_list.append(SearchResult(msg, self._searchbar_input, matched_word, self._case_sensitive, self._selected_color))
                            continue

                    for match in matches:
                        matched_word = match.group()
                        self._search_result_list.append(SearchResult(msg, self._searchbar_input, matched_word, self._case_sensitive, self._selected_color))

                return self._search_result_list
            case FilterType.RULE_ID:
                return None
            case FilterType.CATEGORY:
                msgs = author.get_messages_by_error_category(self._selected_value) #if selected_value is empty -> give all
                for msg in msgs:
                    for error in msg.error_list:
                        startPos = error.start_pos
                        endPos = error.end_pos
                        keyword = msg.content[startPos:endPos]

                        original_content = msg.content
                        content = original_content if self._case_sensitive else original_content.lower()
                        query = keyword if self._case_sensitive else keyword.lower()

                        index = content.find(query)
                        if index != -1:
                            matched_word = original_content[index:index+len(keyword)]
                            self._search_result_list.append(SearchResult(msg, keyword, matched_word, self._case_sensitive, self._selected_color))
                            continue

                return self._search_result_list
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {self._filter_type}")
            
    @staticmethod
    def get_values(filter_type: FilterType, author: Author):
        match filter_type:
            case FilterType.WORD:
                return []
            case FilterType.RULE_ID:
                return author.get_error_rule_ids()
            case FilterType.CATEGORY:
                return author.get_error_categories()
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {self._filter_type}")


