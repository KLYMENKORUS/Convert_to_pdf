from typing import Annotated, Any
from io import BytesIO

from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Response,
    status,
)
from pydantic import EmailStr

from app.utils.format_file import FormatFile
from app.internal.user.dependencies import current_user
from app.database import User
from .dependencies import file_services
from .schemas import FilesModel, ResponseFiles, FileDelete


router = APIRouter(prefix="/file", tags=["File"])


@router.post(
    "/add",
    summary="Add a new file and convert here",
    response_model=ResponseFiles,
)
async def add_files(
    file: Annotated[UploadFile, File(...)],
    format_file: FormatFile,
    file_service: file_services,
    username: EmailStr | None = None,
) -> ResponseFiles:
    await file_service.add_operation(
        filename=file.filename,
        data_file=file,
        format_file=format_file,
        email=username,
    )

    return ResponseFiles(
        response="successfully converting file", status=status.HTTP_200_OK
    )


@router.get("/get", summary="Get file by name")
async def get_file(
    filename: str,
    file_service: file_services,
    username: EmailStr | None = None,
) -> Response:
    file = await file_service.get_operation(email=username, filename=filename)

    content = BytesIO(file).read()

    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


@router.get(
    "/all",
    summary="Get all files by current user",
    response_model=list[FilesModel],
)
async def get_all(
    user: Annotated[User, Depends(current_user())], file_service: file_services
) -> list[FilesModel]:
    user_files = await file_service.all_operation(user_id=user.id)

    return [
        FilesModel(id=file.id, user_email=user.email, filename=file.file_name)
        for file in user_files
    ]


@router.delete(
    "/delete", summary="Deleted file by user", response_model=FileDelete
)
async def delete(
    filename: str,
    user: Annotated[User, Depends(current_user())],
    file_service: file_services,
) -> FileDelete:
    await file_service.file_delete(filename=filename, user_id=user.id)

    return FileDelete(
        status=status.HTTP_200_OK, detail="Delete file successfully"
    )
