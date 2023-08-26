from abc import ABC, abstractmethod
from typing import Any

from tortoise.models import Model


class AbstractRepo(ABC):
    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, field: str, value: Any):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def all_by_filter(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        ...


class TortoiseRepo(AbstractRepo):
    model: Model = None

    async def add(self, *args, **kwargs: Any) -> Model:
        return await self.model.create(**kwargs)

    async def get(self, field: str, value: Any) -> Model:
        return await self.model.get(**{field: value})

    async def delete(self, **kwargs: Any):
        return await self.model.filter(**kwargs).delete()

    async def all_by_filter(self, **kwargs: Any) -> list[Model]:
        return await self.model.filter(user_id=kwargs.get("user_id"))
