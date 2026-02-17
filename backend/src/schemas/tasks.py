from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    description: str
    assigned_to_id: int 
    assigned_by_id: Optional[int] = None 


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    description: Optional[str] = None
    assigned_to_id: Optional[int] = None
    completed_at: Optional[datetime] = None

class TaskComplete(BaseModel):
    completed_at: datetime = datetime.now()

class Task(TaskBase):
    id: int
    assigned_by_id: Optional[int] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TaskWithUsers(Task):
    assigned_by: Optional['User'] = None 
    assigned_to: Optional['User'] = None