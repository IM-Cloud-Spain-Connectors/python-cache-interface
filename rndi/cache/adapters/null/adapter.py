#
# This file is part of the Ingram Micro CloudBlue RnD Integration Connectors SDK.
#
# Copyright (c) 2023 Ingram Micro. All Rights Reserved.
#
from typing import Any, Optional

from rndi.cache.contracts import Cache


class NullCacheAdapter(Cache):  # pragma: no cover
    def has(self, key: str) -> bool:
        return False

    def get(self, key: str, default: Any = None) -> Any:
        value = default() if callable(default) else default

        if isinstance(value, tuple):
            value, ttl = value

        return value

    def put(self, key: str, value: Any, ttl: Optional[int] = None) -> Any:
        return value

    def delete(self, key: str) -> None:
        return None

    def flush(self, expired_only: bool = False) -> None:
        return None
