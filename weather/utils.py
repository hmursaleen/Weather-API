from django.core.cache import cache

def get_from_cache(key):
    """
    Retrieve a value from the cache.
    :param key: Cache key
    :return: Cached value or None if the key doesn't exist
    """
    return cache.get(key)

def set_in_cache(key, value, expiration=43200):
    """
    Store a value in the cache with an expiration time.
    :param key: Cache key
    :param value: Value to store
    :param expiration: Expiration time in seconds (default: 12 hours)
    """
    cache.set(key, value, timeout=expiration)
