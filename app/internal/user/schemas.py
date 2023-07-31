import uuid
from typing import Optional

from pydantic import EmailStr, BaseModel, Field


class UserRead(BaseModel):
    id: uuid.UUID = Field(..., examples=[uuid.uuid4()])
    username: str = Field(..., examples=['nick@1245'])
    email: EmailStr = Field(..., examples=['nick@gmail.com'])
    is_active: Optional[bool] = Field(..., examples=[True])


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str