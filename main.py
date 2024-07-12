from fastapi import FastAPI

from api import api_router


app = FastAPI()


def create_app() -> FastAPI:
    app_ = FastAPI()
    app_.include_router(api_router)

    return app_


app = create_app()