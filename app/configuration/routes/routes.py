from dataclasses import dataclass
from fastapi import FastAPI


@dataclass(frozen=True)
class Routes:

    routes: tuple

    def register_routes(self, app: FastAPI) -> None:
        """Register routes"""
        for router in self.routes:
            app.include_router(router)