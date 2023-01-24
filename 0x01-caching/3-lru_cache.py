#!/usr/bin/env python3
""" mod's doc string """


from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ basic cache class implements a caching system"""
    def __init__(self):
        super().__init__()
        self.lru_lst = []

    def put(self, key, item):
        """ inserts item into self.cache_data """
        if key is None or item is None:
            return

        if len(self.cache_data) < BaseCaching.MAX_ITEMS:
            if self.get(key) is None:
                self.lru_lst.insert(0, key)
            self.cache_data[key] = item
        else:
            if self.get(key) is None:
                to_be_removed = self.lru_lst[-1]
                self.lru_lst.remove(to_be_removed)
                del self.cache_data[to_be_removed]
                self.lru_lst.insert(0, key)
                self.cache_data[key] = item
                print(f"DISCARD: {to_be_removed}")
            else:
                self.re_arrange_lru_lst_on_key_access(key)
                self.cache_data[key] = item

    def get(self, key):
        """ gets item with index == key from self.cached_data """
        if self.cache_data.get(key):
            self.re_arrange_lru_lst_on_key_access(key)
        return self.cache_data.get(key)

    def re_arrange_lru_lst_on_key_access(self, key):
        """ checks if key in lru_list and places it at index  """
        if self.cache_data.get(key):
            self.lru_lst.remove(key)
        else:
            self.lru_lst.remove(self.lru_lst[-1])
        self.lru_lst.insert(0, key)
