from typing import Any, ParamSpec, TypeVar, Callable, Awaitable
from functools import wraps

from fastapi_cache import FastAPICache
from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from fastapi_cache.backends.redis import RedisBackend


P = ParamSpec("P")
R = TypeVar("R")


class ConnectToRedis:
    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            redis = aioredis.from_url("redis://redis:6379/", encoding="utf-8")
            FastAPICache.init(RedisBackend(redis))
            kwargs.update(redis=redis)

            return await func(*args, **kwargs)

        return wrapper


class RedisTools:
    @classmethod
    @ConnectToRedis()
    async def set_pair(cls, file_name: str, file_data: bytes, **kwargs: Any):
        redis: Redis[Any] = kwargs.get("redis")
        return await redis.set(file_name, file_data)

    @classmethod
    @ConnectToRedis()
    async def get_pair(cls, file_name: str, **kwargs: Any):
        redis: Redis[Any] = kwargs.get("redis")
        return await redis.get(file_name)

    @classmethod
    @ConnectToRedis()
    async def get_keys(cls, **kwargs: Any):
        redis: Redis[Any] = kwargs.get("redis")
        return await redis.keys()

    @classmethod
    @ConnectToRedis()
    async def flush(cls, **kwargs: Any):
        redis: Redis[Any] = kwargs.get("redis")
        return await redis.flushdb()

    @classmethod
    @ConnectToRedis()
    async def delete_key(cls, *args: Any, **kwargs: Any):
        redis: Redis[Any] = kwargs.get("redis")
        return await redis.delete(*args)

    @classmethod
    async def task_celery(cls):
        return [
            item for item in await cls.get_keys() if item.startswith(b"celery")
        ]
