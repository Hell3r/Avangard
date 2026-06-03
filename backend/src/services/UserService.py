from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.users import UserModel
from src.schemas.users import UserCreate, UserUpdate
from passlib.context import CryptContext
from typing import Optional, List
from src.services.AuthService import pwd_context
from src.services.EventJournalService import EventJournalService


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
            full_name=getattr(user_data, "full_name", ""),
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

    async def toggle_on_site(self, user_id: int) -> Optional[UserModel]:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        from datetime import datetime
        if user.is_on_site:
            user.is_on_site = False
            user.on_site_since = None
            event = f"{user.full_name} покинул объект"
            event = f"site_left; user_id={user.id}; actor_user_id={user.id}; {event}"
        else:
            # Arrive site
            user.is_on_site = True
            user.on_site_since = datetime.utcnow()
            event = f"{user.full_name} прибыл на объект"
            event = f"site_entered; user_id={user.id}; actor_user_id={user.id}; {event}"

        await self.session.commit()
        await self.session.refresh(user)

        await EventJournalService(self.session).log_event(event)
        return user

    async def transfer(self, user_id: int, address_id: int) -> Optional[UserModel]:
        """Transfer a user to a different address (object)."""
        user = await self.get_by_id(user_id)
        if not user:
            return None
        user.address_id = address_id
        await self.session.commit()
        await self.session.refresh(user)
        # Log the transfer event
        event = f"user_transfer; user_id={user.id}; new_address_id={address_id}; actor_user_id={user.id}; Переведен на другой объект"
        await EventJournalService(self.session).log_event(event)
        return user

    async def get_all_on_site_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """
        Получить всех активных пользователей, которые находятся на любом объекте.
        Доступно только администратору.
        """
        result = await self.session.execute(
            select(UserModel)
            .where(
                and_(
                    UserModel.is_on_site == True,
                    UserModel.is_active == True
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(UserModel.on_site_since)
        )
        return result.scalars().all()

    async def get_all_active_users(self, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Получить все активные пользователи (для статистики)."""
        result = await self.session.execute(
            select(UserModel)
            .where(UserModel.is_active == True)
            .offset(skip)
            .limit(limit)
            .order_by(UserModel.id)
        )
        return result.scalars().all()

    async def get_on_site_users_by_address(self, address_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Получить активных on-site пользователей на конкретном объекте (по address_id)."""
        result = await self.session.execute(
            select(UserModel)
            .where(
                and_(
                    UserModel.is_on_site == True,
                    UserModel.is_active == True,
                    UserModel.address_id == address_id
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(UserModel.on_site_since)
        )
        return result.scalars().all()

    async def get_off_site_users_by_address(self, address_id: int, skip: int = 0, limit: int = 100) -> List[UserModel]:
        """Получить отсутствующих (is_on_site=False) активных пользователей на конкретном объекте."""
        result = await self.session.execute(
            select(UserModel)
            .where(
                and_(
                    UserModel.is_on_site == False,
                    UserModel.is_active == True,
                    UserModel.address_id == address_id
                )
            )
            .offset(skip)
            .limit(limit)
            .order_by(UserModel.id)
        )
        return result.scalars().all()

