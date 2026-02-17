from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.adresses import AddressModel
from src.schemas.addresses import AddressCreate
from typing import Optional, List


class AddressService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, address_id: int) -> Optional[AddressModel]:
        result = await self.session.execute(
            select(AddressModel).where(AddressModel.id == address_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[AddressModel]:
        result = await self.session.execute(
            select(AddressModel)
            .offset(skip)
            .limit(limit)
            .order_by(AddressModel.id)
        )
        return result.scalars().all()
    
    async def create(self, address_data: AddressCreate) -> AddressModel:
        db_address = AddressModel(name=address_data.name)
        self.session.add(db_address)
        await self.session.commit()
        await self.session.refresh(db_address)
        return db_address
    
    async def delete(self, address_id: int) -> bool:
        address = await self.get_by_id(address_id)
        if address:
            await self.session.delete(address)
            await self.session.commit()
            return True
        return False

