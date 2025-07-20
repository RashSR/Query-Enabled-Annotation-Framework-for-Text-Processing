from __future__ import annotations #is needed so i can use FilterNode in the add_leaf function -> python 3.7+ needed
from .filter_type import FilterType
from .search_result import SearchResult
from .message import Message
import utils
from collections import defaultdict
from mainFlask.data.cachestore import CacheStore

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
            case FilterType.NOT:
                #is special because not can only have one node
                all_messages = CacheStore.Instance().get_all_messages()
                self._leaves[0].get_full_result()
                excluded_messages = self._leaves[0].result_messages
                excluded_ids = {msg.message_id for msg in excluded_messages}
                remaining_messages = [msg for msg in all_messages if msg.message_id not in excluded_ids]
                self._result_messages = remaining_messages
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
                self._search_results = self._calc_and_result()
                return self._search_results
            case FilterType.OR:
                self._search_results = self._calc_or_result()
                return self._search_results
            case FilterType.NOT:
                my_messages = self.result_messages
                for msg in my_messages:
                    sr = SearchResult(msg, msg.content, "")
                    sr.left = msg.content
                    self.search_results.append(sr)

                return self._search_results 
            case FilterType.OBJECT:
                return self.get_result()
            case _: 
                #default case
                return full_result
        
    def _calc_and_result(self) -> list[SearchResult]:
        all_results = self._get_all_search_result_lists()
        conjoined_search_results = self.common_search_results(all_results)
        conjoined_search_results_without_just_messages = self._clean_conjoined_messages(conjoined_search_results)
        return conjoined_search_results_without_just_messages
    
    #for AND, we only care about results inside messages — normal messages are not needed EXCEPT all search results are messages
    def _clean_conjoined_messages(self, conjoined_search_results: list[SearchResult]) -> list[SearchResult]:
        #collect search_results that are just messages
        to_remove = []
        for search_result in conjoined_search_results:
            if search_result.is_just_message():
                to_remove.append(search_result)
        
        #only remove search results that are just messages if there are non message search results
        if len(to_remove) != len(conjoined_search_results):
            for sr in to_remove:
                conjoined_search_results.remove(sr)

        #remove duplicates
        duplicate_free_list = list(set(conjoined_search_results))
        return duplicate_free_list

    def common_search_results(self, nested: list[list[SearchResult]]) -> list[SearchResult]:
        if not nested:
            return []

        num_lists = len(nested)

        # Step 1: Count how many lists each message_id appears in
        message_id_counts = defaultdict(int)
        for sublist in nested:
            unique_ids = set(result.message.message_id for result in sublist)
            for message_id in unique_ids:
                message_id_counts[message_id] += 1

        # Step 2: Determine which message_ids are common to all lists
        common_ids = {message_id for message_id, count in message_id_counts.items() if count == num_lists}

        # Step 3: Collect all SearchResults with common message_ids
        result = [res for sublist in nested for res in sublist if res.message.message_id in common_ids]

        return result
    
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

    def _is_already_in_result_messages(self, new_message: Message):
        for stored_message in self._result_messages:
            if stored_message.message_id == new_message.message_id:
                return True
        return False