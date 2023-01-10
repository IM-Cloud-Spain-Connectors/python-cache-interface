import os
import glob
import re
import time
from typing import Any, Optional

from rndi.cache_interface.contracts import Cache
import jsonpickle


def _get_file_contents(file_name: str) -> Any:
    with open(file_name, 'r') as cache:
        return jsonpickle.decode(cache.read())


def _delete_file(file_name: str) -> None:
    try:
        os.remove(file_name)
    except FileNotFoundError:
        pass


class FileSystemCacheAdapter(Cache):
    def __init__(self, directory_path: str, ttl: int = 900):
        self.directory_path = directory_path.strip().rstrip('/')
        self.ttl = ttl

    def _get_file_name(self, key: str) -> str:
        key = re.sub(r"[:/]", "_", key)
        return f'{self.directory_path}/cache.{key}.json'

    def has(self, key: str) -> bool:
        return self.get(key) is not None

    def get(self, key: str, default: Any = None) -> Any:
        cache_file = self._get_file_name(key)
        try:
            content = _get_file_contents(cache_file)

            if time.time() >= content['expire_at']:
                _delete_file(cache_file)
                raise FileNotFoundError

            return content['value']
        except FileNotFoundError:
            ttl = self.ttl
            value = default() if callable(default) else default

            if isinstance(value, tuple):
                value, ttl = value

        return value if value is None else self.put(key, value, ttl)

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> Any:
        with open(self._get_file_name(key), 'w') as cache:
            cache.write(jsonpickle.encode({
                'expire_at': (self.ttl if ttl is None else ttl) + time.time(),
                'value': value,
            }))

        return value

    def delete(self, key: str) -> None:
        _delete_file(self._get_file_name(key))

    def flush(self, expired_only: bool = False) -> None:
        destroy = _delete_file
        if expired_only:
            def _delete_if_expired(file_name: str) -> None:
                content = _get_file_contents(file_name)

                if time.time() >= content['expire_at']:
                    _delete_file(file_name)

            destroy = _delete_if_expired

        for file in glob.glob(self._get_file_name('*')):
            destroy(file)
