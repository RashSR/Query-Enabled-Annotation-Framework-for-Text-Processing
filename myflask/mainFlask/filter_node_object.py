from myflask.mainFlask.filter_type import FilterType
from classes.message import Message
from classes.author import Author

class FilterNodeObejct:
    def __init__(self, filter_type: FilterType, searchbar, selected_value: str, case_sensitive = False, whole_word = False, use_regex = False):
        self._filter_type = filter_type
        self._searchbar = searchbar
        self._selected_value = selected_value #rigt_side
        self._case_sensitive = case_sensitive
        self._whole_word = whole_word
        self._use_regex = use_regex
        self._result_messages = []

    @property
    def filter_type(self):
        return self._filter_type
    
    @filter_type.setter
    def filter_type(self, value: str):
        self._filter_type = value

    @property
    def searchbar(self):
        return self._searchbar
    
    @searchbar.setter
    def searchbar(self, value: str):
        self._searchbar = value

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

    def __str__(self):
        toString = f"""left side: {self._filter_type}
        searchbar: {self._searchbar}
        selected value: {self._selected_value}
        case_sensitive: {self._case_sensitive}
        whole word: {self._whole_word}
        use regex: {self._use_regex}
        """

        return toString

    def get_result(self, author: Author):
        match self._filter_type:
            case FilterType.WORD:
                return None
            case FilterType.RULE_ID:
                return None
            case FilterType.CATEGORY:
                return author.get_messages_by_error_category(self._selected_value)
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {self._filter_type}")
            
    @staticmethod
    def get_values(filter_type: FilterType, author: Author):
        match filter_type:
            case FilterType.WORD:
                return None
            case FilterType.RULE_ID:
                return author.get_error_rule_ids()
            case FilterType.CATEGORY:
                return author.get_error_categories()
            case _: 
                #default case
                raise ValueError(f"Unknown filter type: {self._filter_type}")


