from datetime import datetime
from typing import Any

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist

from app.database import JWT_SECRET_KEY, ALGORITHM
from app.internal.user.schemas import TokenPayload
from app.repositories.user import UserRepository
from app.utils.auth import Hasher


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


class CurrentUserMiddleware:
    def __init__(self) -> None:
        self.jwt_secret_key = JWT_SECRET_KEY
        self.algorithm = ALGORITHM
        self.user_repo = UserRepository()

    async def __call__(self, token: str = Depends(oauth2_scheme)) -> Any:
        return await self.get_current_user(token)

    async def get_current_user(self, token: str) -> Any:
        try:
            payload = jwt.decode(
                token, self.jwt_secret_key, algorithms=[self.algorithm]
            )
            token_payload = TokenPayload(**payload)

            if datetime.fromtimestamp(token_payload.exp) < datetime.now():
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token expired",
                    headers={"WWW-Authenticate": "Bearer"},
                )

        except (jwt.JWTError, ValidationError):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            user = await self.user_repo.get("email", token_payload.sub)

        except DoesNotExist:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User with does not exist",
            )

        return user


class AuthenticateUser:
    def __init__(self) -> None:
        self.user_repo = UserRepository()
        self.exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
        self.doesnotexist = HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email user does not exist",
        )

    async def __call__(self, **kwargs) -> Any:
        return await self.auth_user(**kwargs)

    async def auth_user(self, **kwargs) -> Any:
        try:
            user = await self.user_repo.get("email", kwargs.get("email"))

            if not Hasher.verify_password(
                kwargs.get("password"), user.hashed_password
            ):
                raise self.exception

        except DoesNotExist:
            raise self.doesnotexist

        return user
