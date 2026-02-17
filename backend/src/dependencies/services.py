from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.services.UserService import UserService
from typing_extensions import Annotated
from src.database.database import get_session

SessionDep = Annotated[AsyncSession, Depends(get_session)]




async def get_user_service(session: SessionDep) -> UserCRUD:
    return UserService(session)

UserServiceDep = Annotated[UserService, Depends(get_user_service)]