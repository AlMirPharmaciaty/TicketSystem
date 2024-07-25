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

    def update_user(self, user: User, new_details: UserUpdate):
        if new_details.username:
            user.username = new_details.username
        if new_details.email:
            user.email = new_details.email
        if new_details.password:
            if user.password != new_details.password:
                user.password = encrypt(new_details.password)
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
