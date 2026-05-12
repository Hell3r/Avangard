from __future__ import annotations

from src.schemas.users import User

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskBase(BaseModel):
    description: str
    assigned_to_id: int

    assigned_by_id: Optional[int] = None

    # Срок сдачи
    due_at: datetime

    # Статус
    status: str = "В работе"



class TaskCreate(BaseModel):
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None

    due_at: Optional[datetime] = None
    status: Optional[str] = None


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None

    due_at: Optional[datetime] = None
    status: Optional[str] = None

    completed_at: Optional[datetime] = None


class TaskComplete(BaseModel):
    completed_at: datetime = datetime.now()


class Task(TaskBase):
    id: int
    assigned_by_id: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None

    # фронт берет assigned_to.full_name
    assigned_to: Optional["User"] = None

    class Config:
        from_attributes = True


class TaskWithUsers(Task):
    # модель оставлена на будущее
    assigned_by: Optional["User"] = None
    assigned_to: Optional["User"] = None

