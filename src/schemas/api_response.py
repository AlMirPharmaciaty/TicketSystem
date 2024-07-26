from pydantic import BaseModel


class APIResponse(BaseModel):
    """Custom API response structure"""
    status: str | None = None
    message: str | None = None
    data: list | None = None
