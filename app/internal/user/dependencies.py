from app.repositories.user import UserRepository
from app.services import UserService


def user_service():
    return UserService(UserRepository)