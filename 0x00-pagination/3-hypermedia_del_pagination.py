#!/usr/bin/env python3
"""
Deletion-resilient hypermedia pagination
"""

import csv
import math
from typing import List, Dict, Any


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper_index(self, index: int = 0, page_size: int = 10) -> Dict:
        """ returns copied section of dataset as a dict """
        dct: Dict[str, Any] = {}
        data = self.dataset()
        offset = index + page_size
        indexed_data = self.indexed_dataset()
        max_index = len(indexed_data) - 1
        assert (isinstance(index, int) and index <= max_index)
        dct["index"] = index
        dct["data"] = []
        dct["page_size"] = page_size
        dct["next_index"] = None

        keys = list(indexed_data.keys())
        try:
            index_of_index = keys.index(index)
        except Exception as e:
            index_of_index = index
            pass

        assert (index_of_index < len(keys) and index_of_index >= 0)
        try:
            next_index = keys[index_of_index + page_size]
        except Exception:
            next_index = None
        stop_index = index_of_index + page_size
        dct["next_index"] = next_index
        for i in keys[index_of_index:stop_index]:
            dct["data"].append(indexed_data[i])

        return dct
