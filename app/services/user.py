from typing import Any

from app.utils import AbstractRepo
from app.utils.auth import UserAlreadyExists, Hasher


class UserService:
    def __init__(self, user_repo: AbstractRepo):
        self.user_repo: AbstractRepo = user_repo()

    @UserAlreadyExists()
    async def create_user(self, **kwargs: Any):
        return await self.user_repo.add(
            username=kwargs.get("username"),
            email=kwargs.get("email"),
            hashed_password=Hasher.get_hashed_pass(kwargs.get("password")),
        )

    async def get_user(self, *args: Any):
        return await self.user_repo.get(*args)
