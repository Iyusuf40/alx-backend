#!/usr/bin/env python3
""" mod's doc string """


from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ basic cache class implements a caching system"""
    def __init__(self):
        super().__init__()

    def put(self, key, item):
        """ inserts item into self.cache_data """
        if key is None or item is None:
            return
        self.cache_data[key] = item

    def get(self, key):
        """ gets item with index == key from self.cached_data """
        return self.cache_data.get(key)
