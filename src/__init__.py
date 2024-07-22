from fastapi import FastAPI
from .utils.database import init_db
from .api import auth


def my_app():

    init_db()

    app = FastAPI()
    app.include_router(auth.auth)

    return app
