from pydantic import BaseModel
from datetime import datetime


class TicketHistoryDetails(BaseModel):
    id: int
    ticket_id: int
    created_at: datetime
    user_id: str
    username: str
    status: str
