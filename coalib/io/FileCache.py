import os

__all__ = ['get_content', 'clear_cache']


# The cache. Maps filenames to either a thunk which will provide source code,
# or a tuple (size, mtime, contents, fullname) once loaded.
cache = {}


def clear_cache():
    """
    Clear the cache entirely.
    """
    global cache
    cache = {}


def get_content(filename):
    """
    Get the raw contents of a file from the cache.
    Update the cache if it doesn't contain an entry for this file already.
    """
    if filename in cache:
        return cache[filename][2]
    return update_cache(filename)


def update_cache(filename):
    """
    Update a cache entry and return its list of lines.
    If something's wrong, print a message, discard the cache entry,
    and return an empty list.
    """
    stat = os.stat(filename)

    with open(filename, 'rb') as fp:
        lines = fp.read()
    size, mtime = stat.st_size, stat.st_mtime
    cache[filename] = size, mtime, lines, filename
    return lines
