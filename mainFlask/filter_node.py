from .filter_type import FilterType
from .search_result import SearchResult
from .filter_node_object import FilterNodeObject
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
                return self.calc_and_result()
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
            
    def calc_and_result(self):

        all_results : list[list[SearchResult]] = []
        for fn in self._leaves:
            leaf_result = fn.get_full_result()
            all_results.append(leaf_result)

        
        if len(all_results) == 1:
            return all_results[0]
        
        conjoined_result = []
        for search_result_list in all_results:
            for search_result in search_result_list:
                isContainedInAllLists: bool = False
                #foreach(ConcurrentObservableCollection<ComponentEqcViewModel> cmps in eqcLists){
                #   isContainedInAllLists = IsContainedInAllLists(eqcLists, cmp);
                #}
                #if(isContainedInAllLists && !ListContainsEQC(result, cmp)){
                #   result.Add(cmp);
                #}

        return all_results

    



