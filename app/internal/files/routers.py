from typing import Annotated, Any
from io import BytesIO

from fastapi import APIRouter, Depends, UploadFile, File, Response, status
from pydantic import EmailStr

from app.utils.format_file import FormatFile
from .dependencies import OperationFiles


router = APIRouter(prefix='/file', tags=['File'])


@router.post('/add', summary='Add a new file and convert here')
async def add_files(
    file: Annotated[UploadFile, File(...)],
    format_file: FormatFile,
    file_service: Annotated[OperationFiles, Depends(OperationFiles)],
    username: EmailStr | None = None
) -> dict[str, Any]:

    await file_service.add_operation(
        filename=file.filename, data_file=file,
        format_file=format_file, email=username
    )

    return {
        'response': 'successfully converting file',
        'status': status.HTTP_200_OK
    }


@router.get('/get', summary='Get file by name')
async def get_file(
        filename: str,
        file_service: Annotated[OperationFiles, Depends(OperationFiles)],
        username: EmailStr | None = None
) -> Response:
    
    file = await file_service.get_operation(email=username, filename=filename)

    content = BytesIO(file).read()

    return Response(
        content=content,
        media_type='application/pdf',
        headers={'Content-Disposition': f'attachment; filename="{filename}"'}
    )
