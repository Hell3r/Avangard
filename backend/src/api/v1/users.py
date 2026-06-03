from typing_extensions import List

from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.database.deps import SessionDep
from src.dependencies.services import UserServiceDep
from src.dependencies.auth import get_current_user

from src.schemas.users import UserCreate, User, UserBase
from src.services.AuthService import (
    add_to_blacklist,
    oauth2_scheme,
    create_access_token,
    authenticate_user,
    check_username_exists
)

import logging
from datetime import datetime

from src.services.UserService import UserService

router = APIRouter(prefix="/v1/users", tags=["Пользователи"])
logger = logging.getLogger(__name__)


@router.post("/login", summary="Авторизация")
async def login_user(
    request: Request,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    try:
        user = await authenticate_user(form_data.username, form_data.password, session)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный username или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Аккаунт деактивирован")

        access_token = create_access_token(data={"sub": user.username})
        user.last_login = datetime.utcnow()
        await session.commit()

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": {
                "username": user.username,
                "full_name": user.full_name,
                "user_id": user.id,
                "avatar_path": user.avatar_path,
                "role": user.role,
                "is_active": user.is_active,
                "last_login": user.last_login,
                "address_id": user.address_id,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при входе в систему",
        )


@router.post("/logout", summary="Выход из системы")
async def logout(token: str = Depends(oauth2_scheme)):
    await add_to_blacklist(token)
    return {"message": "Успешный выход из системы"}


@router.get("/me", response_model=User, summary="Получить текущего пользователя")
async def get_current_user_info(current_user=Depends(get_current_user)):
    return current_user


@router.get("/active", response_model=List[User], summary="Все активные пользователи")
async def get_all_active_users(service: UserServiceDep, skip: int = 0, limit: int = 100):
    return await service.get_all_active_users(skip=skip, limit=limit)


@router.put("/me/on-site", response_model=User, summary="Переключить on-site для себя")
async def toggle_on_site(service: UserServiceDep, current_user=Depends(get_current_user)):
    updated_user = await service.toggle_on_site(current_user.id)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return updated_user


@router.get("/on-site", response_model=List[User], summary="Сотрудники мастера на объекте")
async def get_master_on_site_users(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user),
):
    if current_user.role != "master":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только master")

    if current_user.address_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У master не указан адрес объекта")

    return await service.get_on_site_users_by_address(
        address_id=current_user.address_id,
        skip=skip,
        limit=limit,
    )

@router.get("/on-site/all", response_model=List[User], summary="Все сотрудники на объекте")
async def get_all_on_site_users(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100,
):
    return await service.get_all_on_site_users(skip=skip, limit=limit)

@router.get("/off-site", response_model=List[User], summary="Отсутствующие сотрудники мастера на объекте")
async def get_master_off_site_users(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_user),
):
    if current_user.role != "master":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только master")

    if current_user.address_id is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="У master не указан адрес объекта")

    return await service.get_off_site_users_by_address(
        address_id=current_user.address_id,
        skip=skip,
        limit=limit,
    )



@router.post("/user", response_model=User, status_code=status.HTTP_201_CREATED, summary="Создание пользователя")
async def create_user(
    service: UserServiceDep,
    session: SessionDep,
    user_data: UserCreate
):
    existing_user = await check_username_exists(user_data.username, session)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким именем уже существует"
        )
        
    new_user = await service.create(user_data)
    
    return new_user

# Transfer user to another address
@router.put("/{user_id}/transfer", response_model=User, summary="Перевести пользователя на другой объект")
async def transfer_user(
    user_id: int,
    address_id: int,
    service: UserServiceDep,
    current_user=Depends(get_current_user),
):
    updated = await service.transfer(user_id, address_id)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return updated
