from uuid import UUID, uuid4

from pydantic import BaseModel, Field, EmailStr
from fastapi import status


class FilesModel(BaseModel):
    id: UUID = Field(..., examples=[uuid4()])
    user_email: EmailStr = Field(..., examples=["user@example.com"])
    filename: str = Field(..., examples=["file-sample"])


class ResponseFiles(BaseModel):
    response: str = Field(
        ...,
        examples=[
            "success",
        ],
    )
    status: int = Field(
        ...,
        examples=[
            200,
        ],
    )


class FileDelete(BaseModel):
    status: int = Field(..., examples=[status.HTTP_200_OK])
    detail: str = Field(..., examples=["Delete operation successfully"])
