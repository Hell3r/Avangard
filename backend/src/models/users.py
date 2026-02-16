from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import Date, Boolean, String, DateTime, Integer
from datetime import date, datetime
from typing import List, Optional


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(index = True)
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default = "common", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    avatar_path: Mapped[Optional[str]] = mapped_column(String(500), default = "static/default_avatar.png" )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}' )"