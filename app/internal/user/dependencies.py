from typing import Type

from app.repositories.user import UserRepository
from app.services import UserService
from app.utils.auth.current_user import CurrentUserMiddleware, AuthenticateUser


def user_service() -> Type[UserService]:
    return UserService(UserRepository)


def current_user() -> Type[CurrentUserMiddleware]:
    return CurrentUserMiddleware()


def authenticate() -> Type[AuthenticateUser]:
    return AuthenticateUser()
