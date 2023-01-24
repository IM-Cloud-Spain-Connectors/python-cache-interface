#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from logging import LoggerAdapter
from typing import Callable, Dict, Optional

from rndi.cache.adapters.fs.adapter import provide_fs_cache_adapter
from rndi.cache.adapters.null.adapter import provide_none_cache_adapter
from rndi.cache.contracts import Cache


def provide_cache(
        config: dict,
        logger: LoggerAdapter,
        drivers: Optional[Dict[str, Callable[[dict], Cache]]] = None,
) -> Cache:
    supported: Dict[str, Callable[[dict], Cache]] = {
        'file': provide_fs_cache_adapter,
        'none': provide_none_cache_adapter,
    }

    if isinstance(drivers, dict):
        supported.update(drivers)

    driver = config.get('CACHE_DRIVER', 'none')
    provider = supported.get(driver)

    if provider is None:
        def _unsupported_driver(_: dict) -> Cache:
            raise ValueError(f"Unsupported cache driver {driver}")

        provider = _unsupported_driver

    try:
        adapter = provider(config)
        logger.debug(f"Cache service configured with {driver} driver.")
    except Exception as e:
        adapter = provide_none_cache_adapter(config)
        logger.error(f"Cache service failure, disabling cache with driver {driver} due to: {e}")

    return adapter
