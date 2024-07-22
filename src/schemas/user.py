from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    pass


class UserDetails(UserBase):
    id: int
    username: str
    email: str
    deleted: bool


class UserCreate(UserBase):
    username: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(min_length=4)


class UserUpdate(UserBase):
    username: str | None = Field(default=None, min_length=4, max_length=16)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=4)
