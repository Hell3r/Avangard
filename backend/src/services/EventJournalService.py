from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.users import UserModel
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
    
    
    async def get_all_events(self, skip: int = 0, limit: int = 100, from_at: str = None, to_at: str = None):
        result = await self.session.execute(
            select(EventJournalModel)
            .offset(skip)
            .limit(limit)
            .order_by(EventJournalModel.event_at.desc())
            .where(
                and_(
                    EventJournalModel.event_at >= from_at if from_at else True,
                    EventJournalModel.event_at <= to_at if to_at else True))
        )
        return result.scalars().all()

