#!/usr/bin/env python3
""" mod's doc string """


from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ basic cache class implements a caching system"""
    def __init__(self):
        super().__init__()
        self.fifo_lst = []

    def put(self, key, item):
        """ inserts item into self.cache_data """
        if key is None or item is None:
            return

        if len(self.cache_data) < BaseCaching.MAX_ITEMS:
            if self.get(key) is None:
                self.fifo_lst.append(key)
            else:
                self.fifo_lst.remove(key)
                self.fifo_lst.append(key)
            self.cache_data[key] = item
        else:
            if self.get(key) is None:
                to_be_removed = self.fifo_lst[0]
                self.fifo_lst.remove(to_be_removed)
                del self.cache_data[to_be_removed]
                self.fifo_lst.append(key)
                self.cache_data[key] = item
                print(f"DISCARD: {to_be_removed}")
            else:
                self.cache_data[key] = item
                self.fifo_lst.remove(key)
                self.fifo_lst.append(key)

    def get(self, key):
        """ gets item with index == key from self.cached_data """
        return self.cache_data.get(key)
