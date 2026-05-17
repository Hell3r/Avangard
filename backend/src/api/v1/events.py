from typing import List, Optional
from fastapi import APIRouter

from src.database.deps import SessionDep
from src.services.EventJournalService import EventJournalService
from src.schemas.events import EventJournal


router = APIRouter(prefix="/v1/events", tags=["Журнал событий"])



@router.get("/", response_model=List[EventJournal], summary="Получить журнал событий")
async def get_events(
    session: SessionDep,

    from_at: Optional[str] = None,
    to_at: Optional[str] = None,

    skip: int = 0,
    limit: int = 100,
):
    service = EventJournalService(session)
    return await service.get_all_events(from_at=from_at, to_at=to_at, skip=skip, limit=limit)



