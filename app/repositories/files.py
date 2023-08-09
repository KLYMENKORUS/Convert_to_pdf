from app.database import File
from app.utils import TortoiseRepo


class FileRepository(TortoiseRepo):
    model = File
