class FilterNodeObejct:
    def __init__(self, left_side, searchbar, selected_value: str, case_sensitive = False, whole_word = False, use_regex = False):
        self._left_side = left_side
        self._searchbar = searchbar
        self._selected_value = selected_value #rigt_side
        self._case_sensitive = case_sensitive
        self._whole_word = whole_word
        self._use_regex = use_regex

    @property
    def left_side(self):
        return self._left_side
    
    @left_side.setter
    def left_side(self, value: str):
        self._left_side = value

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

    def __str__(self):
        toString = f"""left side: {self._left_side}
        searchbar: {self._searchbar}
        selected value: {self._selected_value}
        case_sensitive: {self._case_sensitive}
        whole word: {self._whole_word}
        use regex: {self._use_regex}
        """

        return toString

    def get_result(self):
        return None
