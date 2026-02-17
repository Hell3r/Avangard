from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.users import UserModel
from src.schemas.users import UserCreate, UserUpdate
from passlib.context import CryptContext
from typing import Optional, List
from src.services.AuthService import pwd_context

class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, user_id: int) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_username(self, username: str) -> Optional[UserModel]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        result = await self.session.execute(
            select(UserModel)
            .offset(skip)
            .limit(limit)
            .order_by(UserModel.id)
        )
        return result.scalars().all()
    
    async def create(self, user_data: UserCreate) -> UserModel:

        hashed_password = pwd_context.hash(user_data.password)
        

        db_user = UserModel(
            username=user_data.username,
            password=hashed_password,
            role=user_data.role,
            address_id=user_data.address_id,
            is_active=True,
            completed_tasks=0
        )
        
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)
        
        return db_user
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[UserModel]:

        user = await self.get_by_id(user_id)
        if not user:
            return None
        

        update_data = user_data.dict(exclude_unset=True)

        if "password" in update_data:
            update_data["password"] = pwd_context.hash(update_data["password"])
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
            return True
        return False
