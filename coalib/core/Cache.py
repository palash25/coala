import pickle
import pickletools

class LRUCache:

    def __init__(self, optimize=False):
        self._cache = {}
        self._accessed = set()
        self._optimize= optimize

    def __getitem__(self, key):
        """
        Record the element access and return the requested item
        """
        self._accessed.add(key)
        return self._cache[key]

    def __setitem__(self, key, value):
        self._cache[key] = value

    def __delitem__(self, key):
        del self._cache[key]

    def evict_items(self):
        """
        Removes the non-accessed cache entries.
        """
        for k in self._cache.keys():
            if k not in self._accessed:
                del self._cache[k]

    def save(self, filename):
        """
        Pickles the cache data and stores it in a file.
        """
        pickled_cache = pickle.dumps(self._cache)
        if self._optimize:
            pickled_cache = pickletools.optimize(pickled_cache)

        with open(filename, 'wb') as f:
            f.write(pickled_cache)
        f.close()
