from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.storage import StorageModel
from src.schemas.storage import StorageCreate, StorageUpdate
from typing import Optional, List


from src.services.EventJournalService import EventJournalService


class StorageService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, storage_id: int) -> Optional[StorageModel]:
        result = await self.session.execute(
            select(StorageModel).where(StorageModel.id == storage_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[StorageModel]:
        result = await self.session.execute(
            select(StorageModel)
            .offset(skip)
            .limit(limit)
            .order_by(StorageModel.id)
        )
        return result.scalars().all()
    
    async def create(self, storage_data: StorageCreate, actor_user_id: Optional[int] = None) -> StorageModel:
        db_storage = StorageModel(**storage_data.dict())
        self.session.add(db_storage)
        await self.session.commit()
        await self.session.refresh(db_storage)

        await EventJournalService(self.session).log_event(
            f"storage_created; storage_id={db_storage.id}; actor_user_id={actor_user_id}; material_name={db_storage.material_name}; remainder={db_storage.remainder}"
        )

        return db_storage
    
    
    async def update(self, storage_id: int, storage_data: StorageUpdate, actor_user_id: Optional[int] = None) -> Optional[StorageModel]:
        storage = await self.get_by_id(storage_id)
        if not storage:
            return None
        
        update_data = storage_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(storage, field, value)
        
        await self.session.commit()
        await self.session.refresh(storage)

        await EventJournalService(self.session).log_event(
            f"storage_updated; storage_id={storage.id}; actor_user_id={actor_user_id}; material_name={storage.material_name}; remainder={storage.remainder}"
        )

        return storage
    
    async def delete(self, storage_id: int, actor_user_id: Optional[int] = None) -> bool:
        storage = await self.get_by_id(storage_id)
        if storage:
            material_name = storage.material_name
            remainder = storage.remainder
            await self.session.delete(storage)
            await self.session.commit()

            await EventJournalService(self.session).log_event(
                f"storage_deleted; storage_id={storage_id}; actor_user_id={actor_user_id}; material_name={material_name}; remainder={remainder}"
            )

            return True
        return False


