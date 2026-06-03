from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import DateTime, Integer, ForeignKey, Text
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional


class StorageWithdrawalModel(Base):
    __tablename__ = "storage_withdrawals"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    storage_id: Mapped[int] = mapped_column(Integer, ForeignKey("storage.id", ondelete="CASCADE"))
    withdrawn_by_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer)
    withdrawn_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    note: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    storage: Mapped["StorageModel"] = relationship("StorageModel", back_populates="withdrawals")
    withdrawn_by: Mapped[Optional["UserModel"]] = relationship("UserModel", back_populates="withdrawals")
