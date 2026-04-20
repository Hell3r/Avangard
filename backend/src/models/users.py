from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import Date, Boolean, String, DateTime, Integer, ForeignKey
from datetime import date, datetime
from typing import List, Optional


class UserModel(Base):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(index = True)
    password: Mapped[str] = mapped_column()
    role: Mapped[str] = mapped_column(default = "common", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    avatar_path: Mapped[Optional[str]] = mapped_column(String(500), default = "static/default_avatar.png" )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"))
    completed_tasks: Mapped[int] = mapped_column(Integer)
    
    
    address: Mapped["AddressModel"] = relationship("AddressModel", back_populates="user")
    assigned_tasks: Mapped[List["TaskModel"]] = relationship("TaskModel", foreign_keys="TaskModel.assigned_by_id", back_populates="assigned_by")
    my_tasks: Mapped[List["TaskModel"]] = relationship("TaskModel", foreign_keys="TaskModel.assigned_to_id", back_populates="assigned_to")
    
    
    def __repr__(self) -> str:
        return f"User(id={self.id}, username='{self.username}' )"
 