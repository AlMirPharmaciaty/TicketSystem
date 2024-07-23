from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models.user import User
from ..utils.encryption import encrypt
from ..schemas.user import UserCreate, UserUpdate
from sqlalchemy import func


def get_user(
    db: Session,
    user_id: int = None,
    username: str = None,
    skip: int = 0,
    limit: int = 10,
):
    query = db.query(User).filter(User.deleted == False)
    if user_id:
        query = query.filter(User.id == user_id)
    if username:
        query = query.filter(User.username == username)
    users = query.offset(skip).limit(limit).all()
    return users


def create_user(db: Session, user: UserCreate):
    user_exists = db.query(User).filter(User.email == user.email).first()

    if user_exists:
        raise HTTPException(
            status_code=400, detail="Please contact support to reactivate your account."
        )
    user = User(**user.model_dump(), roles=["Customer"])
    user.password = encrypt(user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user: UserUpdate, user_id=int):
    old_user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not old_user:
        raise HTTPException(status_code=400, detail="User not found.")

    if user.username:
        old_user.username = user.username
    if user.email:
        old_user.email = user.email
    if user.password:
        if old_user.password != user.password:
            old_user.password = encrypt(user.password)
    db.commit()
    db.refresh(old_user)
    return old_user


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id, User.deleted == False).first()

    if not user:
        raise HTTPException(status_code=400, detail="User not found.")

    user.deleted = True
    db.commit()
    return user


def manage_user_roles(db: Session, user_id: int, roles: list[str]):
    pass