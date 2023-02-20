#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Any, Optional

from rndi.cache.contracts import Cache


def provide_none_cache_adapter(_: dict) -> Cache:
    return NullCacheAdapter()


class NullCacheAdapter(Cache):  # pragma: no cover
    def has(self, key: str) -> bool:
        return False

    def get(self, key: str, default: Any = None, ttl: Optional[int] = None) -> Any:
        value = default() if callable(default) else default

        if isinstance(value, tuple):
            value, _ = value

        return value

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> Any:
        return value

    def delete(self, key: str) -> None:
        return None

    def flush(self, expired_only: bool = False) -> None:
        return None
