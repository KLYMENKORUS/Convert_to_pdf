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
        self.message_error = "User with this email: {} already exist"

    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            try:
                if await self.user_service.get("email", kwargs.get("email")):
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=self.message_error.format(kwargs.get("email")),
                    )
            except DoesNotExist:
                return await func(*args, **kwargs)

        return wrapper


class CheckUser:
    def __init__(self):
        self.user_service = UserRepository()
        self.exception = HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with does not exist",
        )

    def __call__(
        self, func: Callable[P, Awaitable[R]]
    ) -> Callable[P, Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs):
            try:
                if user := await self.user_service.get(
                    "email", kwargs.get("email")
                ):
                    kwargs.update(user=user)
                    return await func(*args, **kwargs)

            except DoesNotExist:
                raise self.exception

        return wrapper
