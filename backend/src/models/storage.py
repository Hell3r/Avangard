from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import Date, Boolean, String, DateTime, Integer
from datetime import date, datetime
from typing import List, Optional



class StorageModel(Base):
    __tablename__ = "storage"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    remainder: Mapped[int] = mapped_column(Integer)
    
    def __repr__(self) -> str:
        return f"Material(id={self.id}, name='{self.material_name}', reminder='{self.remainder}')" 