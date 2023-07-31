from typing import Annotated, Any
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, Response, status
from pydantic import EmailStr

from app.services import FileService, FileServiceRedis
from .dependencies import file_service, redis_service


router = APIRouter(prefix='/file', tags=['File'])


@router.post('/add', summary='Add a new file and convert here')
async def add_files(
        file_serv: Annotated[FileService, Depends(file_service)],
        file: Annotated[UploadFile, File(...)],
        redis_serv: Annotated[FileServiceRedis, Depends(redis_service)]
) -> dict[str, Any]:

    # await service.create_file(file_name=file.filename, data_file=file)
    await redis_serv.write_to_redis(filename=file.filename.split('.')[0], data_file=file)

    return {
        'response': 'successfully converting file',
        'status': status.HTTP_200_OK
    }


@router.get('/get', summary='Get file by name')
async def get_file(
        filename: str,
        redis_serv: Annotated[FileServiceRedis, Depends(redis_service)]
) -> Response:

    file = await redis_serv.get_file_redis(filename=filename)
    content = BytesIO(file).read()

    return Response(
        content=content,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
