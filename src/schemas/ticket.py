from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from src.schemas.ticket_status import TicketStatus

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

class TicketUpdate(BaseModel):
    status: TicketStatus

class TicketCreate(TicketBase):
    pass

class TicketOrder(str, Enum):
    OLD = "Oldest"
    LAT = "Latest"
