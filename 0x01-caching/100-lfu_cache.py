#!/usr/bin/env python3
""" mod's doc string """


from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """ basic cache class implements a caching system"""
    def __init__(self):
        super().__init__()
        self.lfu_lst = []

    def put(self, key, item):
        """ inserts item into self.cache_data """
        if key is None or item is None:
            return

        if len(self.cache_data) < BaseCaching.MAX_ITEMS:
            if self.get(key) is None:
                self.lfu_lst.insert(0, (key, 0))
            self.cache_data[key] = item
        else:
            if self.get(key) is None:
                to_be_removed = self.re_arrange_lfu_lst_on_key_access(key)
                del self.cache_data[to_be_removed[0]]
                self.cache_data[key] = item
                print(f"DISCARD: {to_be_removed[0]}")
            else:
                self.re_arrange_lfu_lst_on_key_access(key)
                self.cache_data[key] = item

    def get(self, key):
        """ gets item with index == key from self.cached_data """
        if self.cache_data.get(key):
            self.re_arrange_lfu_lst_on_key_access(key)
        return self.cache_data.get(key)

    def re_arrange_lfu_lst_on_key_access(self, key):
        """ checks if key in lfu_list and places it at index  0 """
        removed = self.remove_key_count_tuple(key)
        return removed

    def remove_key_count_tuple(self, key):
        """ searches for key in a list of key, count tuple pair
        and removes the tuple """
        idx = 0
        found = False
        itm_tuple = (key, 0)
        for item in self.lfu_lst:
            if item[0] == key:
                found = True
                itm_tuple = item
                break
            idx += 1
        if found:
            removed = self.lfu_lst[idx]
            self.lfu_lst.pop(idx)
            current_count = itm_tuple[1] + 1
            itm_tuple = (key, current_count)
        else:
            removed = self.scan_lowest_count()
            # print("scan --- ", removed, self.lfu_lst)
            self.lfu_lst.remove(removed)

        self.lfu_lst.insert(0, itm_tuple)
        return removed

    def scan_lowest_count(self):
        """ returns the key_count tuple with lowest count """
        min = self.lfu_lst[0][1]
        key_count = None
        for key, count in self.lfu_lst:
            if min >= count:
                key_count = (key, count)
                min = count

        return key_count
