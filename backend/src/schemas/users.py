from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional, List, ForwardRef
import re


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Имя пользователя")
    avatar_path: Optional[str] = Field("static/default_avatar.png", description="Путь к аватару")
    address_id: int = Field(..., description="ID адреса")
    completed_tasks: int = Field(0, description="Количество выполненных задач")
    
    @validator('username')
    def validate_username(cls, v):
        if not re.match("^[a-zA-Z0-9_]+$", v):
            raise ValueError('Username must contain only letters, numbers and underscore')
        return v

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, description="Пароль пользователя")
    address_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    password: Optional[str] = Field(None, min_length=6)
    role: Optional[str] = None
    is_active: Optional[bool] = None
    avatar_path: Optional[str] = None
    address_id: Optional[int] = None
    completed_tasks: Optional[int] = None
    
    @validator('password')
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters')
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isupper() for char in v):
            raise ValueError('Password must contain at least one uppercase letter')
        return v

class User(UserBase):
    id: int
    role: str = "common"
    is_active: bool = True
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None 
    
    class Config:
        from_attributes = True



class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    user_id: Optional[int] = None
    role: Optional[str] = None

