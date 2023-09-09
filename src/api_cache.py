from time import time
from json import dumps
from functools import wraps
from inspect import signature
from typing import Type, TypeVar, Optional

from pydantic import BaseModel, parse_file_as

from .logger import logger
from .define import CACHE_DIR
from .utils import DateTimeEncoder, generate_cache_name

T = TypeVar('T')


def save_cache(name: str, data: str) -> None:
    """保存缓存"""
    if not CACHE_DIR.exists():
        CACHE_DIR.mkdir()
    cache_file = CACHE_DIR / f'{name}.cache'
    with cache_file.open('w', encoding='utf-8') as f:
        f.write(data)


def get_cache(name: str, model: Type[T], ttl: int) -> Optional[T]:
    """获取缓存"""
    cache_file = CACHE_DIR / f'{name}.cache'
    if cache_file.exists() and time() - cache_file.stat().st_ctime < ttl:
        return parse_file_as(model, cache_file)
    return None


def use_cache(model: Type[T], ttl: int):
    """装饰器"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            cache_name = generate_cache_name(
                func.__name__,
                signature(func).bind(*args, **kwargs).arguments,
            )
            cache = get_cache(cache_name, model, ttl)
            if cache is None:
                cache = await func(*args, **kwargs)
                if isinstance(cache, BaseModel):
                    data = cache.json()
                # elif isinstance(cache, list):
                else:  # 目前其余情况只有List[Model]
                    data = dumps(
                        [data.dict() for data in cache],
                        cls=DateTimeEncoder,
                    )
                save_cache(cache_name, data)
            else:
                logger.debug(f'{func.__name__} 使用缓存')
            return cache

        return wrapper

    return decorator


# 还没想好怎么用
# def clear_cache(name: str) -> None:
#     """清除缓存"""
#     cache_file = CACHE_DIR / f'{name}.cache'
#     if cache_file.exists():
#         cache_file.unlink()
