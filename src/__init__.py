from fastapi import FastAPI
from .utils.database import init_db
from .api import auth, user


def my_app():

    init_db()

    app = FastAPI()
    app.include_router(auth.auth)
    app.include_router(user.users)

    return app
