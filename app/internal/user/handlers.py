from typing import Annotated

from fastapi import APIRouter, Depends

from .schemas import UserRead, UserCreate
from .dependencies import user_service
from app.services import UserService


router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register', summary='Create a new user', response_model=UserRead)
async def register(
        body: UserCreate,
        service: Annotated[UserService, Depends(user_service)]
) -> UserRead:

    user = await service.create_user(**body.model_dump())

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active
    )