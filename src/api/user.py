from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..utils.database import get_db
from ..schemas.user import UserDetails, UserUpdate, UserRolesUpdate
from ..controllers.user import update_user, delete_user, get_user, manage_user_roles
from ..models.user import User
from ..utils.auth import get_current_user, RoleChecker

users = APIRouter(prefix="/user", tags=["User"])


@users.get("/", response_model=list[UserDetails])
def users_get_all(
    db: Session = Depends(get_db),
    user_id: int = None,
    username: str = None,
    skip: int = 0,
    limit: int = 10,
):
    return get_user(db=db, user_id=user_id, username=username, skip=skip, limit=limit)


@users.put("/", response_model=UserDetails)
def user_update(
    user: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_user(db=db, user=user, user_id=current_user.id)


@users.delete("/", response_model=UserDetails)
def user_delete(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return delete_user(db=db, user_id=user.id)


@users.post("/roles/", response_model=UserDetails)
def user_role_manager(
    user_id: int,
    roles: UserRolesUpdate,
    db: Session = Depends(get_db),
    _=Depends(RoleChecker(allowed_roles=["Admin"])),
):
    return manage_user_roles(db=db, user_id=user_id, roles=roles)
