from .filter_type import FilterType
from .search_result import SearchResult
from .filter_node_object import FilterNodeObject
from functools import reduce
from __future__ import annotations #is needed so i can use FilterNode in the add_leaf function -> python 3.7+ needed

class FilterNode:
    def __init__(self, filter_type: FilterType):
        self._filter_type = filter_type
        self._leaves : list[FilterNode] = []

    @property
    def filter_type(self) -> FilterType:
        return self._filter_type
    
    @filter_type.setter
    def filter_type(self, value: FilterType):
        self._filter_type = value

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
                return self._calc_and_result()
            case FilterType.OR:
                return full_result
            case FilterType.NOT:
                return full_result
            case FilterType.OBJECT:
                fno = (FilterNodeObject)(self)
                return fno.get_result()
            case _: 
                #default case
                return full_result
            
    def _calc_and_result(self):

        all_results = self._get_all_search_result_lists()

        if len(all_results) == 1:
            return all_results[0]
        
        #intersects all lists and conjoins them
        conjoined_result = list(reduce(lambda a, b: a & b, map(set, all_results)))

        return conjoined_result
    
    def _get_all_search_result_lists(self) -> list[list[SearchResult]]:
        all_results : list[list[SearchResult]] = []
        
        for fn in self._leaves:
            leaf_result = fn.get_full_result()
            all_results.append(leaf_result)

        return all_results

    



