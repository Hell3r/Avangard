from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime

from src.database.database import Base


class EventJournalModel(Base):
    __tablename__ = "event_journal"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    # Описание события: строго одно поле TEXT, куда будем складывать всё необходимое
    # (например: "task_completed; task_id=...; actor=...; ...")
    event_description: Mapped[str] = mapped_column(nullable=False, default="")

    event_at: Mapped[datetime] = mapped_column(nullable=False, server_default=func.now())

