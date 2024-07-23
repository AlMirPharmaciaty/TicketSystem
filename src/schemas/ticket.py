from pydantic import BaseModel
from datetime import datetime


class TicketBase(BaseModel):
    title: str
    description: str


class TicketDetails(TicketBase):
    id: int
    status: str
    user_id: str
    username: str
    created_at: datetime


class TicketCreate(TicketBase):
    pass
