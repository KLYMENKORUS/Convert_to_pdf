from fastapi import FastAPI
from app.configuration.server import Server
import uvicorn


def create_app(_=None) -> FastAPI:
    """Create app FastAPI"""

    app = FastAPI(title='Convert to PDF')

    return Server(app).get_app()


if __name__ == '__main__':
    uvicorn.run(app=create_app(), port=7000, host='127.0.0.1',)