from fastapi import APIRouter


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/get')
async def get():
    return {'status': 'ok'}