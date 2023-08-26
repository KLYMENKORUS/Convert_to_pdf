from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import UserRead, UserCreate, TokenSchemas, UserDelete
from .dependencies import user_service, authenticate, current_user
from app.services import UserService
from app.database import ACCESS_TOKEN_EXPIRE_MINUTES, User
from app.utils.auth.token import Token


router = APIRouter(prefix="/user", tags=["user"])


@router.post("/register", summary="Create a new user", response_model=UserRead)
async def register(
    body: UserCreate, service: Annotated[UserService, Depends(user_service)]
) -> UserRead:
    user = await service.create_user(**body.model_dump())

    return UserRead(
        id=user.id,
        username=user.username,
        email=user.email,
        is_active=user.is_active,
    )


@router.post("/login", summary="Login user", response_model=TokenSchemas)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_user=Depends(authenticate),
) -> TokenSchemas:
    user = await auth_user(
        email=form_data.username, password=form_data.password
    )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Token(
        user.email, access_token_expires
    ).create_access_token()

    return TokenSchemas(access_token=access_token, token_type="Bearer")


@router.delete("/delete", summary="Delete by user", response_model=UserDelete)
async def delete_user(
    user: Annotated[User, Depends(current_user())],
    service: Annotated[UserService, Depends(user_service)],
) -> UserDelete:
    await service.delete(email=user.email)

    return UserDelete(
        status=status.HTTP_200_OK, detail="Delete user successfully"
    )
