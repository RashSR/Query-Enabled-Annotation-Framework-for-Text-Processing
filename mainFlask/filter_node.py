from .filter_mode import FilterMode
from .search_result import SearchResult


class FilterNode:
    def __init__(self, filter_mode: FilterMode):
        self._filter_mode = filter_mode
        self._filterNodeObjects = []

    def get_full_result(self) -> list[SearchResult]:
        match self._filter_mode:
            case FilterMode.AND:
                return None
            case FilterMode.OR:
                return None
            case FilterMode.NOT:
                return None
            case FilterMode.OBJECT:
                return None
            case _: 
                #default case
                return None


