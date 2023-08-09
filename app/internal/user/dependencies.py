from app.repositories.user import UserRepository
from app.services import UserService
from app.utils.auth.current_user import CurrentUserMiddleware, AuthenticateUser


def user_service():
    return UserService(UserRepository)


def current_user():
    return CurrentUserMiddleware()


def authenticate():
    return AuthenticateUser()