from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from datetime import datetime
from typing import Optional
from src.models.events_journal import EventJournalModel




class EventJournalService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def log_event(self, description: str) -> EventJournalModel:
        event = EventJournalModel(event_description=description)
        self.session.add(event)
        await self.session.commit()
        await self.session.refresh(event)
        return event
    
    
    async def get_all_events(
        self,
        skip: int = 0,
        limit: int = 100,
        from_at: str = None,
        to_at: str = None,
    ):
        def _parse_dt(value: Optional[str]):

            if not value:
                return None
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                return datetime.fromisoformat(value + "T00:00:00")

        parsed_from = _parse_dt(from_at)
        parsed_to = _parse_dt(to_at)

        conditions = []
        if parsed_from is not None:
            conditions.append(EventJournalModel.event_at >= parsed_from)
        if parsed_to is not None:
            conditions.append(EventJournalModel.event_at <= parsed_to)

        stmt = (
            select(EventJournalModel)
            .offset(skip)
            .limit(limit)
            .order_by(EventJournalModel.event_at.desc())
        )

        if conditions:
            stmt = stmt.where(and_(*conditions))

        result = await self.session.execute(stmt)
        return result.scalars().all()


