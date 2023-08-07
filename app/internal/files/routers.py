from typing import Annotated, Any
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, Response, status
from pydantic import EmailStr

from app.services import FileService, FileServiceRedis
from app.utils.format_file import FormatFile
from .dependencies import file_service, redis_service


router = APIRouter(prefix='/file', tags=['File'])


@router.post('/add', summary='Add a new file and convert here')
async def add_files(
    file: Annotated[UploadFile, File(...)],
    format_file: FormatFile,
    file_serv: Annotated[FileService, Depends(file_service)],
    redis_serv: Annotated[FileServiceRedis, Depends(redis_service)],
    username: EmailStr | None = None
) -> dict[str, Any]:
    
    if username is None:
        await redis_serv.write_to_redis(
            filename=file.filename, data_file=file,
            format_file=format_file)
    
    else:
        await file_serv.create_file(
            filename=file.filename, data_file=file,
            email=username, format_file=format_file)

    return {
        'response': 'successfully converting file',
        'status': status.HTTP_200_OK
    }


@router.get('/get', summary='Get file by name')
async def get_file(
        filename: str,
        redis_serv: Annotated[FileServiceRedis, Depends(redis_service)],
        file_serv: Annotated[FileService, Depends(file_service)],
        username: EmailStr | None = None
) -> Response:
    
    file = None

    if username is None:
        file = await redis_serv.get_file_redis(filename=filename)
    else:
        file = await file_serv.get_file_db(email=username, file_name=filename)

    content = BytesIO(file).read()

    return Response(
        content=content,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
