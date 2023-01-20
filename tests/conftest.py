#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import List

import pytest

from rndi.cache.adapters.fs.adapter import FileSystemCacheAdapter
from rndi.cache.adapters.null.adapter import NullCacheAdapter
from rndi.cache.contracts import Cache


@pytest.fixture
def adapters():
    def __adapters() -> List[Cache]:
        return [
            FileSystemCacheAdapter('/tmp'),
            NullCacheAdapter(),
        ]

    return __adapters
