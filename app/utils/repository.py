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
        if kwargs.get("file_name"):
            return await self.model.get(file_name=kwargs.get("file_name"))
        else:
            return await self.model.get(email=kwargs.get("email"))

    async def delete(self, *args, **kwargs):
        return await self.model.filter(
            file_name=kwargs.get("filename"), user_id=kwargs.get("user_id")
        ).delete()

    async def all_by_filter(self, **kwargs):
        return await self.model.filter(user_id=kwargs.get("user_id"))
