from app.database import User
from app.utils import TortoiseRepo


class UserRepository(TortoiseRepo):
    model = User