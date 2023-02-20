#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Optional, Union
from logging import LoggerAdapter
from unittest.mock import patch

import pytest
from rndi.cache.adapters.fs.adapter import FileSystemCacheAdapter, get_file_contents
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


@pytest.fixture
def adapters(logger):
    def __adapters() -> List[Union[Cache, HasEntry]]:
        setups = [
            {'CACHE_DRIVER': 'file', 'CACHE_DIR': '/tmp'},
            {'CACHE_DRIVER': 'none'},
        ]

        extra = {
            'file': provide_test_fs_cache_adapter,
        }

        return [provide_cache(setup, logger(), extra) for setup in setups]

    return __adapters


@pytest.fixture()
def logger():
    def __logger() -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            return logger

    return __logger


class HasEntry(metaclass=ABCMeta):  # pragma: no cover
    @abstractmethod
    def get_entry(self, key: str) -> Optional[Dict[str, Union[str, int]]]:
        """
        Get an entry from the cache, not only the value.
        This is useful for testing purposes when we want to validate the TTL.
        :param key: str The key to search for.
        :return: Optional[Dict[str, Union[str, int]]] The entry if found, None otherwise.
        """


class FileSystemCacheAdapterTester(FileSystemCacheAdapter, HasEntry):
    def get_entry(self, key: str) -> Optional[Dict[str, Union[str, int]]]:
        cache_file = self._get_file_name(key)

        content = get_file_contents(cache_file)

        return {
            'value': content['value'],
            'expire_at': content['expire_at'],
        }


def provide_test_fs_cache_adapter(config: dict) -> Cache:
    return FileSystemCacheAdapterTester(
        directory_path=config.get('CACHE_DIR', '/tmp/cache'),
        ttl=config.get('CACHE_TTL', 900),
    )
