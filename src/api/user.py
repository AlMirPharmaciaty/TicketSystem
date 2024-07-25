from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from src.utils.database import get_db
from src.utils.auth import get_current_user, RoleChecker
from src.models.user import User
from src.schemas.api_response import APIResponse
from src.schemas.user import UserUpdate, UserRolesUpdate
from src.controllers.user import UserController

users = APIRouter(prefix="/user", tags=["User"])


@users.get("/", response_model=APIResponse)
def users_get_all(
    db: Session = Depends(get_db),
    user_id: int = None,
    username: str = None,
    email: str = None,
    skip: int = 0,
    limit: int = 10,
    _=Depends(RoleChecker(allowed_roles=["Pharmacist", "Admin"])),
):
    response = APIResponse()
    try:
        controller = UserController(db=db)
        data = controller.get_user(
            user_id=user_id,
            username=username,
            email=email,
            skip=skip,
            limit=limit,
        )
        response.data = jsonable_encoder(data)
        response.status = "status"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@users.put("/", response_model=APIResponse)
def user_update(
    new_details: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response = APIResponse()
    try:
        controller = UserController(db=db)
        user = controller.get_user(user_id=current_user.id)

        if not user:
            raise Exception("User not found.")

        if new_details.email:
            duplicate_email = (
                db.query(User)
                .filter(User.id != current_user.id, User.email == new_details.email)
                .first()
            )
            if duplicate_email:
                raise Exception("Email already exists.")

        data = controller.update_user(user=user[0], new_details=new_details)
        response.data = jsonable_encoder([data])
        response.status = "status"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@users.delete("/", response_model=APIResponse)
def user_delete(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    response = APIResponse()
    try:
        controller = UserController(db=db)
        user = controller.get_user(user_id=user.id)
        if not user:
            raise Exception("User not found.")

        data = controller.delete_user(user=user[0])
        response.data = jsonable_encoder([data])
        response.status = "status"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response


@users.post("/roles/", response_model=APIResponse)
def user_role_manager(
    user_id: int,
    roles: UserRolesUpdate,
    db: Session = Depends(get_db),
    _=Depends(RoleChecker(allowed_roles=["Admin"])),
):
    response = APIResponse()
    try:
        controller = UserController(db=db)
        user = controller.get_user(user_id=user_id)
        if not user:
            raise Exception("User not found.")

        data = controller.manage_user_roles(user=user[0], roles=roles)
        response.data = jsonable_encoder([data])
        response.status = "success"

    except Exception as e:
        response.status = "error"
        response.message = e.args[0]

    return response
