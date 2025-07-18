from .filter_node_group import FilterNodeGroup
from .filter_node import FilterNode
from .filter_type import FilterType
from .message import Message
from .search_result import SearchResult
from mainFlask.data.cachestore import CacheStore
from mainFlask.settings import Settings
import re

class FilterNodeObject(FilterNode):
    def __init__(self, filter_node_group: FilterNodeGroup, searchbar_input, selected_value: str, case_sensitive = False, whole_word = False, use_regex = False):
        super().__init__(FilterType.OBJECT)
        self._filter_node_group = filter_node_group
        self._searchbar_input = searchbar_input
        self._selected_value = selected_value #rigt_side
        self._case_sensitive = case_sensitive
        self._whole_word = whole_word
        self._use_regex = use_regex
        self._search_result_list = []
        self._selected_color = Settings.Instance()._get_next_color()

    @property
    def filter_node_group(self) -> FilterNodeGroup:
        return self._filter_node_group
    
    @filter_node_group.setter
    def filter_node_group(self, value: str) -> None:
        self._filter_node_group = value

    @property
    def searchbar_input(self) -> str:
        return self._searchbar_input
    
    @searchbar_input.setter
    def searchbar_input(self, value: str) -> None:
        self._searchbar_input = value

    @property
    def selected_value(self) -> str:
        return self._selected_value
    
    @selected_value.setter
    def selected_value(self, value: str) -> None:
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
    def search_result_list(self) -> list[SearchResult]:
        return self._search_result_list
    
    @search_result_list.setter
    def search_result_list(self, value: list[SearchResult]) -> None:
        self._search_result_list = value

    @property
    def selected_color(self) -> str:
        return self._selected_color
    
    @selected_color.setter
    def selected_color(self, value: str) -> None:
        self._selected_color = value

    def __str__(self):
        toString = f"""left side: {self._filter_node_group}
        searchbar: {self._searchbar_input}
        selected value: {self._selected_value}
        case_sensitive: {self._case_sensitive}
        whole word: {self._whole_word}
        use regex: {self._use_regex}
        """

        return toString

    @staticmethod
    def get_values(filter_node_group: FilterNodeGroup):
        match filter_node_group:
            case (FilterNodeGroup.WORD | FilterNodeGroup.EMOJI):
                #enables textfield
                return []
            case FilterNodeGroup.RULE_ID:
                return CacheStore.Instance().get_all_distinct_rule_ids_from_ltms()
            case FilterNodeGroup.CATEGORY:
                return CacheStore.Instance().get_all_distinct_categories_from_ltms()
            case FilterNodeGroup.AUTHOR | FilterNodeGroup.RECIPIENT:
                author_names = []
                all_authors = CacheStore.Instance().get_all_authors()
                for author in all_authors:
                    author_names.append(author.name)

                return author_names 
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {filter_node_group}")

    def get_result(self) -> list[SearchResult]:
        match self._filter_node_group:
            case FilterNodeGroup.WORD:
                if not self._use_regex and not self._case_sensitive and not self._whole_word:
                    # Not regex, not whole word: simple substring
                    my_msgs = CacheStore.Instance().get_messages_by_substring_in_content(self._searchbar_input)
                    for msg in my_msgs:
                        text = msg.content
                        pattern = self._searchbar_input

                        matches = re.finditer(pattern, text, re.IGNORECASE)
                    
                        for match in matches:
                            matched_word = match.group()
                            sr = SearchResult(msg, self._searchbar_input, matched_word, self._case_sensitive, self._selected_color, start_pos=match.start(), end_pos=match.end()-1)
                            self._add_search_results_messages(sr)
                    return []

                for msg in CacheStore.Instance().get_all_messages():
                    original_content = msg.content
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
                        

                    for match in matches:
                        matched_word = match.group()
                        sr = SearchResult(msg, self._searchbar_input, matched_word, self._case_sensitive, self._selected_color)
                        self._add_search_results_messages(sr)

                return self._search_result_list
            case FilterNodeGroup.RULE_ID:
                return self._filter_by_error_attr('rule_id')
            case FilterNodeGroup.CATEGORY:
                return self._filter_by_error_attr('category')
            case FilterNodeGroup.EMOJI:
                return []
            case FilterNodeGroup.AUTHOR:
                #TODO Maybe change result table? msg jump only works if active author is selected right
                author = CacheStore.Instance().get_author_by_name(self._selected_value)
                messages = author.get_all_own_messages()
                self._convert_messages_into_search_results(messages)
                return self._search_result_list
            case FilterNodeGroup.RECIPIENT:
                author = CacheStore.Instance().get_author_by_name(self._selected_value)
                messages = CacheStore.Instance().get_messages_by_recipient_id(author.id)
                self._convert_messages_into_search_results(messages)
                return self._search_result_list
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {self._filter_node_group}")

    def _convert_messages_into_search_results(self, messages):
        for msg in messages:
            sr = SearchResult(msg, msg.content, "")
            sr.left = msg.content
            self._add_search_results_messages(sr)

    def _filter_by_error_attr(self, attr_name):
        if attr_name == 'rule_id':
            loaded_msgs = CacheStore.Instance().get_messages_by_error_rule_id(self._selected_value)
        elif attr_name == 'category':
            loaded_msgs = CacheStore.Instance().get_messages_by_error_category(self._selected_value)
        else:
            return []

        for msg in loaded_msgs:
            for error in msg.error_list:
                if getattr(error, attr_name) == self._selected_value:
                    self._convert_error_to_search_result(error, msg)
        
        return self._search_result_list
    
    def _convert_error_to_search_result(self, error, msg: Message):
        startPos = error.start_pos
        endPos = error.end_pos
        keyword = msg.content[startPos:endPos]

        original_content = msg.content
        content = original_content

        index = content.find(keyword)
        if index != -1:
            matched_word = original_content[index:index+len(keyword)]
            sr = SearchResult(msg, keyword, matched_word, self._case_sensitive, self._selected_color, start_pos=startPos, end_pos=endPos)
            self._add_search_results_messages(sr)

    def _add_search_results_messages(self, sr: SearchResult):
        message = CacheStore.Instance().get_message_by_id(sr.message.message_id)
        if not sr in self._search_result_list:
            self._search_result_list.append(sr)
        if not sr in message.search_results:
            message.search_results.append(sr)
        if not self._is_already_in_result_messages(message):
            self._result_messages.append(message)

    def _is_already_in_result_messages(self, new_message: Message):
        for stored_message in self._result_messages:
            if stored_message.message_id == new_message.message_id:
                return True
        return False
    
    def __str__(self):
        toString = f"filter_node_group: {self._filter_node_group}, input: {self._searchbar_input}, selected_value: {self._selected_value}"
        return toString
            

