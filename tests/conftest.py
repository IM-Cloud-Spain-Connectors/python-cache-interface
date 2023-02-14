#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import List
from logging import LoggerAdapter
from unittest.mock import patch

import pytest
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


@pytest.fixture
def adapters(logger):
    def __adapters() -> List[Cache]:
        setups = [
            {'CACHE_DRIVER': 'file', 'CACHE_DIR': '/tmp'},
            {'CACHE_DRIVER': 'none'},
        ]

        return [provide_cache(setup, logger()) for setup in setups]

    return __adapters


@pytest.fixture()
def logger():
    def __logger() -> LoggerAdapter:
        with patch('logging.LoggerAdapter') as logger:
            return logger

    return __logger
