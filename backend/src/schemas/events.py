from datetime import datetime
from pydantic import BaseModel


class EventJournal(BaseModel):
    id: int
    event_description: str
    event_at: datetime

