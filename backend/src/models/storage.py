from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database.database import Base
from sqlalchemy import Integer
from typing import List


class StorageModel(Base):
    __tablename__ = "storage"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    material_name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    remainder: Mapped[int] = mapped_column(Integer)

    withdrawals: Mapped[List["StorageWithdrawalModel"]] = relationship("StorageWithdrawalModel", back_populates="storage")

    def __repr__(self) -> str:
        return f"Material(id={self.id}, name='{self.material_name}', remainder='{self.remainder}')"