from datetime import timedelta, datetime
from typing import Any, Optional

from jose import jwt

from app.database import JWT_SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


class Token:
    def __init__(
        self, subject: str | Any, expires_delta: Optional[timedelta] = None
    ) -> None:
        self.subject = subject
        self.expires_delta = expires_delta
        self.expire = None

    def create_access_token(self) -> str:
        if self.expires_delta:
            self.expire = datetime.utcnow() + self.expires_delta
        else:
            self.expire = datetime.utcnow() + timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode = dict(exp=self.expire, sub=str(self.subject))

        return jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
