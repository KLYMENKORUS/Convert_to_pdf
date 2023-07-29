from abc import ABC, abstractmethod

from tortoise.models import Model


class AbstractRepo(ABC):

    @abstractmethod
    async def add(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, *args, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def all_by_filter(self, *args, **kwargs):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        ...


class TortoiseRepo(AbstractRepo):

    model: Model = None

    async def add(self, *args, **kwargs):
        return await self.model.create(**kwargs)

    async def get(self, *args, **kwargs):
        return await self.model.get(file_name=kwargs.get('file_name'))

    async def delete(self, *args, **kwargs):
        return await self.model.delete()

    async def all_by_filter(self, *args, **kwargs):
        return self.model.filter(user=kwargs.get('user'))

