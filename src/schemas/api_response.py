from pydantic import BaseModel


class APIResponse(BaseModel):
    status: str | None = None
    message: str | None = None
    data: list | None = None