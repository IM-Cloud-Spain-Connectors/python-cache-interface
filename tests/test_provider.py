from rndi.cache.adapters.fs.adapter import FileSystemCacheAdapter
from rndi.cache.adapters.null.adapter import NullCacheAdapter
from rndi.cache.contracts import Cache
from rndi.cache.provider import provide_cache


def test_make_cache_should_make_a_cache_adapter(logger):
    cache = provide_cache({
        'CACHE_DRIVER': 'file'
    }, logger())

    assert isinstance(cache, Cache)
    assert isinstance(cache, FileSystemCacheAdapter)


def test_make_cache_should_use_null_cache_on_invalid_cache_configuration(logger):
    cache = provide_cache({
        'CACHE_DRIVER': 'wrong'
    }, logger())

    assert isinstance(cache, Cache)
    assert isinstance(cache, NullCacheAdapter)


def test_make_cache_should_correctly_make_cache_adapter_with_extra_drivers(logger):
    class CustomCache(NullCacheAdapter):
        pass

    cache = provide_cache({'CACHE_DRIVER': 'custom'}, logger(), {'custom': lambda _: CustomCache()})

    assert isinstance(cache, Cache)
    assert isinstance(cache, CustomCache)
