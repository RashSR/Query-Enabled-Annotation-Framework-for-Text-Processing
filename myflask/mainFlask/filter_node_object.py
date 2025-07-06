class FilterNodeObejct:
    def __init__(self, left_side, searchbar, selected_value: str):
        self._left_side = left_side
        self._searchbar = searchbar
        self._selected_value = selected_value #rigt_side

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

    def get_result(self):
        return None
