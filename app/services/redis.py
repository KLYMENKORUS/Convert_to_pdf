from typing import ParamSpec, TypeVar, Callable, Awaitable
from functools import wraps

from fastapi_cache import FastAPICache
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend


P = ParamSpec("P")
R = TypeVar("R")


class ConnectToRedis:

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            redis = aioredis.from_url('redis://redis:6379/', encoding='utf-8')
            FastAPICache.init(RedisBackend(redis))
            kwargs.update(redis=redis)

            return await func(*args, **kwargs)

        return wrapper


class RedisTools:

    @classmethod
    @ConnectToRedis()
    async def set_pair(cls, file_name: str, file_data: bytes, **kwargs):
        return await kwargs.get('redis').set(file_name, file_data)

    @classmethod
    @ConnectToRedis()
    async def get_pair(cls, file_name: str, **kwargs):
        return await kwargs.get('redis').get(file_name)

    @classmethod
    @ConnectToRedis()
    async def get_keys(cls, **kwargs):
        return await kwargs.get('redis').keys()
