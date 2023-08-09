from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr


class FilesModel(BaseModel):
    id: UUID = Field(..., examples=[uuid4()])
    user_email: EmailStr = Field(..., examples=["user@example.com"])
    filename: str = Field(..., examples=["file-sample"])
