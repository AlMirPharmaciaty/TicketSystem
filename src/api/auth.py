from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.auth import authenticate_user, create_access_token
from src.models.user import User
from src.schemas.api_response import APIResponse
from src.schemas.user import UserCreate
from src.schemas.auth import Token
from src.controllers.user import UserController

auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/register/", response_model=APIResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    API for users to create a new account
    """
    response = APIResponse()

    try:
        user_exists = db.query(User).filter(User.email == user.email).first()
        if user_exists:
            raise Exception("Email already exists.")

        controller = UserController(db=db)
        data = controller.create_user(user=user)
        response.data = jsonable_encoder([data])
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@auth.post("/login/", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    API to let users log into the system
    they are first authenticated by username and password
    if verified, a JWT token is created and sent to them
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")
