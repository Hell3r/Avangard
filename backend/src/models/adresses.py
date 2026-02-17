from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import Date, Boolean, String, DateTime, Integer
from datetime import date, datetime
from typing import List, Optional


class AddressModel(Base):
    __tablename__ = "addresses"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="address")
    
    def __repr__(self) -> str:
        return f"Address(id={self.id}, name='{self.name}' )"
