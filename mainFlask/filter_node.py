from __future__ import annotations #is needed so i can use FilterNode in the add_leaf function -> python 3.7+ needed
from .filter_type import FilterType
from .search_result import SearchResult
from functools import reduce
from classes.author import Author
from classes.message import Message


class FilterNode:
    def __init__(self, filter_type: FilterType):
        self._filter_type = filter_type
        self._leaves : list[FilterNode] = []
        self._result_messages = []

    @property
    def filter_type(self) -> FilterType:
        return self._filter_type
    
    @filter_type.setter
    def filter_type(self, value: FilterType):
        self._filter_type = value

    @property
    def result_messages(self) -> list[Message]:
        return self._result_messages
    
    @result_messages.setter
    def result_messages(self, value: list[Message]):
        self._result_messages = value

    @property
    def leaves(self) -> list[FilterNode]:
        return self._leaves
    
    @leaves.setter
    def leaves(self, value) -> list[FilterNode]:
        self._leaves = value

    def add_leaf(self, fn: FilterNode):
        self._leaves.append(fn)

    #TODO: don't use author here
    def get_full_result(self, author: Author) -> list[SearchResult]:
        full_result = []
        match self._filter_type:
            case FilterType.AND:
                return self._calc_and_result(author)
            case FilterType.OR:
                return self._calc_or_result(author)
            case FilterType.NOT:
                return full_result
            case FilterType.OBJECT:
                return self.get_result(author)
            case _: 
                #default case
                return full_result
            
    def _calc_and_result(self, author: Author) -> list[SearchResult]:
        all_results = self._get_all_search_result_lists(author)
        #intersects all lists and conjoins them
        conjoined_result = list(reduce(lambda a, b: a & b, map(set, all_results)))
        return conjoined_result
    
    def _calc_or_result(self, author: Author) -> list[SearchResult]:
        all_results = self._get_all_search_result_lists(author)
        all_results_without_duplicates = list(set().union(*all_results))
        return all_results_without_duplicates

    def _get_all_search_result_lists(self, author: Author) -> list[list[SearchResult]]:
        all_results : list[list[SearchResult]] = []
        
        for fn in self._leaves:
            leaf_result = fn.get_full_result(author)
            all_results.append(leaf_result)

        return all_results

    



