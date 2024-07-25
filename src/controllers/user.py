from sqlalchemy.orm import Session

from src.utils.encryption import encrypt
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate, UserRolesUpdate


class UserController:
    def __init__(self, db: Session):
        self.db = db

    def get_user(
        self,
        user_id: int = None,
        username: str = None,
        email: str = None,
        skip: int = 0,
        limit: int = 10,
    ):
        users = self.db.query(User).filter(User.deleted == False)
        if user_id:
            users = users.filter(User.id == user_id)
        if username:
            users = users.filter(User.username == username)
        if email:
            users = users.filter(User.email == email)
        return users.offset(skip).limit(limit).all()

    def create_user(self, user: UserCreate):
        user = User(**user.model_dump(), roles=[])
        user.password = encrypt(user.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_user(self, user: User, user_update: UserUpdate):
        if user_update.username:
            user.username = user_update.username
        if user_update.email:
            user.email = user_update.email
        if user_update.password:
            if user.password != user_update.password:
                user.password = encrypt(user_update.password)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete_user(self, user: User):
        user.deleted = True
        self.db.commit()
        self.db.refresh(user)
        return user

    def manage_user_roles(self, user: User, roles: UserRolesUpdate):
        user.roles = roles.roles
        self.db.commit()
        self.db.refresh(user)
        return user
