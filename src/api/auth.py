from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..schemas.auth import Token
from ..controllers.auth import authenticate_user, create_access_token
from ..controllers.user import create_user
from ..schemas.user import UserDetails, UserCreate

auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/login/", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint to let users log into the system
    they are first authenticated by username and password
    if verified, a token is created and sent to them
    """
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")


@auth.post("/register/", response_model=UserDetails)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
