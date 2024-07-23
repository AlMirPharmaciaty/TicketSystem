import os
from dotenv import load_dotenv
from fastapi import FastAPI
from .utils.database import init_db
from .api import auth, user


def my_app():

    load_dotenv()
    init_db()

    app = FastAPI(title=os.getenv("TITLE"))
    app.include_router(auth.auth)
    app.include_router(user.users)

    return app
