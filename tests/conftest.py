from typing import List

import pytest

from rndi.cache_interface.adapters.fs import FileSystemCacheAdapter
from rndi.cache_interface.adapters.null import NullCacheAdapter
from rndi.cache_interface.contracts import Cache


@pytest.fixture
def adapters():
    def __adapters() -> List[Cache]:
        return [
            FileSystemCacheAdapter('/tmp'),
            NullCacheAdapter(),
        ]

    return __adapters
