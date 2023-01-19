#!/usr/bin/env python3
""" mod's doc string """


import csv
import math
from typing import List, Set, Dict, Tuple, Any


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ computes and returns the range of indexes
    to return in a list for which page and page_size
    was determined """
    end_index = page * page_size
    start_index = end_index - page_size
    return (start_index, end_index)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """ get page returns paginated dataset based on page and page
        size"""
        assert (
            isinstance(page, int) and isinstance(page_size, int)
            and page > 0 and page_size > 0
        )
        start, end = index_range(page, page_size)
        data = self.dataset()
        # max_page = math.ceil(len(data) / page_size)
        if start > len(data) - 2 or end > len(data) - 1:
            return []
        return data[start:end]

    def get_hyper(self, page: int = 1, page_size: int = 10) -> Dict[str,  Any]:
        """ returns a dict consisting of paginated data """
        data = self.get_page(page, page_size)
        all_data = self.dataset()
        max_page = math.ceil(len(all_data) / page_size)
        dct: Dict[str,  Any] = {}
        dct["page_size"] = page_size
        dct["page"] = page
        dct["data"] = data
        dct["total_pages"] = max_page
        dct["next_page"] = None
        dct["prev_page"] = None
        if page > 1:
            dct["prev_page"] = page - 1
        if page < max_page:
            dct["next_page"] = page + 1
        return dct
