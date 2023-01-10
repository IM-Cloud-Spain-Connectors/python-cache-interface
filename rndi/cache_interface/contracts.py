from abc import ABCMeta, abstractmethod
from typing import Any, Optional


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
