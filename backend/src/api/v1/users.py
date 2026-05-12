from typing_extensions import List
from fastapi import APIRouter, HTTPException, status, Depends, Response, Path, Form, File, UploadFile, BackgroundTasks, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select, delete, and_, func
from src.models.users import UserModel
from src.database.deps import SessionDep
from src.dependencies.services import UserServiceDep
from typing import Optional
import logging
import os
import uuid
from datetime import date
from src.schemas.users import UserCreate, User, UserBase
from src.services.AuthService import (
    add_to_blacklist,
    pwd_context,
    oauth2_scheme,
    create_access_token,
    authenticate_user,
    token_blacklist,
    verify_password,
    check_username_exists,
    get_password_hash,
    get_current_user
)

router = APIRouter(prefix="/v1/users", tags=["Пользователи"])
logger = logging.getLogger(__name__)


@router.post("/login", summary="Авторизация")
async def login_user(
    request: Request,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends()
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
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Аккаунт деактивирован",
            )

        access_token = create_access_token(data={"sub": user.username})

        from datetime import datetime
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
                "address_id": user.address_id
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Произошла ошибка при входе в систему")
        
        
        
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


@router.post("/logout", summary="Выход из системы")
async def logout(
    token: str = Depends(oauth2_scheme)
):
    await add_to_blacklist(token)
    return {"message": "Успешный выход из системы"}


@router.get("/me", response_model=User, summary="Получить текущего пользователя")
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user


@router.put("/me/on-site", response_model=User, summary="Переключить статус на объекте")
async def toggle_on_site(
    service: UserServiceDep,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Сотрудник переключает статус 'на объекте' для себя.
    """
    updated_user = await service.toggle_on_site(current_user.id)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")
    return updated_user

@router.get(
    "/on-site/all",
    response_model=List[User],
    summary="Все сотрудники на объектах (только админ)",
    dependencies=[Depends(get_current_user)]  # если нужно явно
)
async def get_all_on_site_users_admin(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Возвращает список всех активных пользователей, у которых is_on_site = True.
    Доступно только администратору.
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только администратор может просматривать всех сотрудников на объектах"
        )
    return await service.get_all_on_site_users(skip, limit)


@router.get(
    "/active",
    response_model=List[User],
    summary="Все активные пользователи для статистики"
)
async def get_all_active_users(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100
):
    return await service.get_all_active_users(skip=skip, limit=limit)


@router.get(
    "/on-site",
    response_model=List[User],
    summary="Сотрудники на объекте текущего мастера"
)
async def get_master_on_site_users(
    service: UserServiceDep,
    skip: int = 0,
    limit: int = 100,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Возвращает список активных пользователей на объекте, к которому привязан мастер.
    Доступно мастеру (и опционально администратору, но тогда нужно передать address_id).
    """
    # Разрешаем доступ только мастеру
    if current_user.role != "master":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Только мастер может просматривать сотрудников на своём объекте"
        )
    
    # Проверяем, что у мастера указан адрес
    if current_user.address_id is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="У мастера не указан адрес объекта"
        )
    
    return await service.get_on_site_users_by_address(
        address_id=current_user.address_id,
        skip=skip,
        limit=limit
    )
