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
        indexed_data = self.__indexed_dataset
        max_index = math.ceil(len(indexed_data) / page_size) - 1
        assert (isinstance(index, int) and index <= max_index)
        dct["index"] = index
        dct["data"] = []
        dct["page_size"] = page_size
        dct["next_index"] = offset

        u_index = set()
        for i in range(index, offset):
            if indexed_data.get(i) and i not in u_index:
                dct["data"].append(indexed_data[i])
                u_index.add(i)
            else:
                if indexed_data.get(i + 1) and (i + 1) not in u_index:
                    dct["data"].append(indexed_data[i + 1])
                    dct["next_index"] = dct["next_index"] + 1
                    u_index.add(i + 1)
                    if i in u_index:  # required to remove double addition
                        dct["next_index"] = dct["next_index"] - 1

        return dct
