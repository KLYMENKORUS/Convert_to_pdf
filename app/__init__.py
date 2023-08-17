import logging

import uvicorn
from fastapi import FastAPI

from app.configuration.server import Server


def create_app(_=None) -> FastAPI:
    """Create app FastAPI"""

    app = FastAPI(title="Convert to PDF")

    return Server(app).get_app()


if __name__ == "__main__":
    logging.basicConfig(
        level="INFO".upper(),
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    uvicorn.run(
        app=create_app(),
        port=7000,
        host="127.0.0.1",
    )
