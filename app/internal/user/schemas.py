import uuid
from typing import Optional
from fastapi import status

from pydantic import EmailStr, BaseModel, Field


class UserRead(BaseModel):
    id: uuid.UUID = Field(..., examples=[uuid.uuid4()])
    username: str = Field(..., examples=["nick@1245"])
    email: EmailStr = Field(..., examples=["nick@gmail.com"])
    is_active: Optional[bool] = Field(..., examples=[True])


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserDelete(BaseModel):
    status: int = Field(..., examples=[status.HTTP_200_OK])
    detail: str = Field(..., examples=["Delete user successfully"])


class TokenSchemas(BaseModel):
    access_token: str = Field(..., examples=[""])
    token_type: str = Field(..., examples=["Bearer"])


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None
