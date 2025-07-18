from __future__ import annotations #is needed so i can use FilterNode in the add_leaf function -> python 3.7+ needed
from .filter_type import FilterType
from .search_result import SearchResult
from functools import reduce
from .message import Message
import utils

class FilterNode:
    def __init__(self, filter_type: FilterType):
        self._filter_type = filter_type
        self._leaves : list[FilterNode] = []
        self._result_messages = []
        self._search_results = []
    
    @property
    def search_results(self) -> list[SearchResult]:
        return self._search_results
    
    @search_results.setter
    def search_results(self, value: list[SearchResult]) -> None:
        self._search_results = value

    @property
    def filter_type(self) -> FilterType:
        return self._filter_type
    
    @filter_type.setter
    def filter_type(self, value: FilterType):
        self._filter_type = value

    @property
    def result_messages(self) -> list[Message]:
        result_message_lists = []       
        for fn in self._leaves:
            result_message_lists.append(fn.result_messages)

        match self._filter_type:
            case FilterType.OR:
                self._result_messages = utils.or_result_messages(result_message_lists)
            case FilterType.AND:
                self._result_messages = utils.and_result_messages(result_message_lists)
            case FilterType.OBJECT:
                return self._result_messages
            case _: 
                #default case
                return []

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

    def get_full_result(self) -> list[SearchResult]:
        full_result = []
        match self._filter_type:
            case FilterType.AND:
                self._calc_and_result()
            case FilterType.OR:
                self._calc_or_result()
            case FilterType.NOT:
                return full_result
            case FilterType.OBJECT:
                return self.get_result()
            case _: 
                #default case
                return full_result
        
        full_result = self._gather_search_results()
        self._search_results = full_result
        return full_result
    
    def _gather_search_results(self) -> list[SearchResult]:
        search_result_list = []
        for msg in self.result_messages:
            for search_result in msg.search_results:
                search_result_list.append(search_result)
        
        return search_result_list

    def _calc_and_result(self) -> list[SearchResult]:
        all_results = self._get_all_search_result_lists()
        #intersects all lists and conjoins them
        conjoined_result = list(reduce(lambda a, b: a & b, map(set, all_results)))
        return conjoined_result
    
    def _calc_or_result(self) -> list[SearchResult]:
        all_results = self._get_all_search_result_lists()
        all_results_without_duplicates = list(set().union(*all_results))
        return all_results_without_duplicates

    def _get_all_search_result_lists(self) -> list[list[SearchResult]]:
        all_results : list[list[SearchResult]] = []
        
        for fn in self._leaves:
            leaf_result = fn.get_full_result()
            all_results.append(leaf_result)

        return all_results
    
    def __str__(self):
        toString = f"Type: {self._filter_type}, Leaves: {len(self._leaves)}"
        return toString
    
    def __repr__(self):
        return f"FilterNode(type={self._filter_type}, leaves={len(self._leaves)})"
    
    def print_leave_structure(self, level = 0):
        indent = self._make_indents(level)
        print(f"{indent}+{self}")
        for fn in self._leaves:
            fn.print_leave_structure(level+1)

    def _make_indents(self, indents: int) -> str:
        return "---" * indents



    



