# Python Cache Interface

[![Test](https://github.com/othercodes/python-cache-interface/actions/workflows/test.yml/badge.svg)](https://github.com/othercodes/python-cache-interface/actions/workflows/test.yml)

Simple and clean Cache interface for python projects.

## Installation

The easiest way to install the Cache Interface is to get the latest version from PyPI:

```bash
# using poetry
poetry add rndi-cache-interface
# using pip
pip install rndi-cache-interface
```

## The Contract

This package provides one simple contract or interface: `Cache`.

```python
class Cache(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def has(self, key: str) -> bool:
        """
        Check if the given key exists in the cache.
        :param key: str The key to search for.
        :return: bool True if the key exists, false otherwise (expired
                      values returns False).
        """

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get the required value by key from the cache.
        :param key: str The key of the stored value.
        :param default: Any The default value to use if the key has no value in
                        cache, None by default. If the default value is a
                        callable, the result value of the execution will
                        be stored in the cache. The expiration time is 900
                        seconds. The callable may return a Tuple[Any, int]
                        with the actual value as first element and the desired
                        expired time as second value.
        :return: Any The requested value by key.
        """

    @abstractmethod
    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> Any:
        """
        Put a value by key in the cache.
        :param key: str The key to store the value.
        :param value: Any The value to store in cache
        :param ttl: int Expiration time in seconds
        :return: Any The stored value by key.
        """

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete a value by key from the cache.
        :param key: str The key to be deleted.
        :return:
        """

    @abstractmethod
    def flush(self, expired_only: bool = False) -> None:
        """
        Delete all the items in the cache.
        :param expired_only: bool If True only the expired values will be deleted.
        :return:
        """
```

## The Adapter

Just initialize the class you want and use the public methods:

```python
from rndi.cache_interface.contracts import Cache
from rndi.cache_interface.adapters.fs import FileSystemCacheAdapter


def some_process_that_requires_cache(cache: Cache):
    # retrieve the data from cache, ir the key is not cached yet and the default 
    # value is a callable the cache will use it to compute and cache the value
    user = cache.get('user-id', lambda: db_get_user('user-id'))

    print(user)


# inject the desired cache adapter.
cache = FileSystemCacheAdapter('/tmp', 900)
some_process_that_requires_cache(cache)
```

Checking the if the key exists in the cache.

```python
cache.has('user-id')
```

Getting a value from the cache.

```python
# will return None if the value not exists in the cache.
cache.get('user-id')

# if the key is not present, the default value will be used.
cache.get('user-id', {'id': 'user-id', 'email': 'vincent.vega@mail.com'})

# if the default value is a callable the cache will use the callable to 
# compute and cache the request value.
cache.get('user-id', lambda: db_get_user('user-id'))

# you can also provide custom ttl (time to live) for a computed value by 
# returning a tuple of computed value and the ttl integer (Tuple[Any, int]).
cache.get('user-id', lambda: (db_get_user('user-id'), 3600))
```

Storing value by key in cache.

```python
# store the given value by key.
cache.put('user-id', {'id': 'user-id', 'email': 'vincent.vega@mail.com'})

# store the given value with custom ttl (time to live).
cache.put('user-id', {'id': 'user-id', 'email': 'vincent.vega@mail.com'}, 3600)
```

Delete a value from cache by key.

```python
cache.delete('user-id')
```

Flush the complete cache.

```python
cache.flush()
```

