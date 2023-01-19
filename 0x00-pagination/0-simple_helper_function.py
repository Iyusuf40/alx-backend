#!/usr/bin/env python3
""" mod's doc string """


from typing import List, Set, Dict, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    """ computes and returns the range of indexes
    to return in a list for which page and page_size
    was determined """
    end_index = page * page_size
    start_index = end_index - page_size
    if start_index < 0:
        start_index = 0
    return (start_index, end_index)
