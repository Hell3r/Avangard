from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.UserService import UserService
from src.services.AddressService import AddressService
from typing_extensions import Annotated
from src.database.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]


async def get_user_service(session: SessionDep) -> UserService:
    return UserService(session)

async def get_address_service(session: SessionDep) -> AddressService:
    return AddressService(session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AddressServiceDep = Annotated[AddressService, Depends(get_address_service)]
