from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import DateTime, Integer, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional


class SiteVisitModel(Base):
    __tablename__ = "site_visits"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    address_id: Mapped[int] = mapped_column(Integer, ForeignKey("addresses.id", ondelete="CASCADE"))
    entered_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    left_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="site_visits")
    address: Mapped["AddressModel"] = relationship("AddressModel", back_populates="site_visits")
