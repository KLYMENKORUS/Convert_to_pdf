from typing import ParamSpec, TypeVar, Callable, Awaitable
from functools import wraps

from fastapi import HTTPException, status
from tortoise.exceptions import DoesNotExist


from app.repositories.user import UserRepository


P = ParamSpec("P")
R = TypeVar("R")


class UserAlreadyExists:

    def __init__(self):
        self.user_service = UserRepository()

    def __call__(self, func: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            try:
                if await self.user_service.get(**kwargs):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f'User with this email: {kwargs.get("email")} already exist'
                    )
            except DoesNotExist:
                return await func(*args, **kwargs)

        return wrapper