from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserRead, UserCreate, TokenSchemas
from .dependencies import user_service, authenticate
from app.services import UserService
from app.database import ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.auth.token import Token


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


@router.post('/login', summary='Login user', response_model=TokenSchemas)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_user = Depends(authenticate)
) -> TokenSchemas:
    
    user = await auth_user(email=form_data.username, password=form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token(user.email, access_token_expires).create_access_token()

    return TokenSchemas(
        access_token=access_token,
        token_type='Bearer'
    )