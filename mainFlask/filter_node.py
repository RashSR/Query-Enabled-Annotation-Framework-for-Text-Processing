from .filter_type import FilterType
from .search_result import SearchResult


class FilterNode:
    def __init__(self, filter_type: FilterType):
        self._filter_type = filter_type
        self._filterNodeObjects = []

    def get_full_result(self) -> list[SearchResult]:
        match self._filter_type:
            case FilterType.AND:
                return None
            case FilterType.OR:
                return None
            case FilterType.NOT:
                return None
            case FilterType.OBJECT:
                return None
            case _: 
                #default case
                return None
            


