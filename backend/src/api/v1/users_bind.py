from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated

from src.dependencies.auth import get_current_user
from src.dependencies.services import UserServiceDep
from src.schemas.users import UserBase




router = APIRouter(prefix="/v1/users", tags=["Пользователи"])


@router.put(
    "/master/bind-address",
    response_model=UserBase,
    summary="Привязать адрес выбранному мастеру (full_name вводит администратор)"
)
async def bind_address_to_master(
    address_id: int,
    master_full_name: str,
    service: UserServiceDep,
    current_user: Annotated[object, Depends(get_current_user)],
):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Только администратор может привязывать адрес мастеру")

    all_users = await service.get_all(skip=0, limit=5000)
    # master_full_name может указывать на пользователя, который изначально был employee.
    # Роль должна быть присвоена в этой ручке, поэтому на этапе поиска НЕ фильтруем по role == "master".
    master = next((u for u in all_users if getattr(u, "full_name", None) == master_full_name), None)


    if not master:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Мастер по full_name не найден")

    updated = await service.update(
        user_id=master.id,
        user_data=UserBase(
            username=master.username,
            full_name=getattr(master, "full_name", ""),
            address_id=address_id,
            role="master",
            completed_tasks=getattr(master, "completed_tasks", 0),
            is_on_site=getattr(master, "is_on_site", False),
            on_site_since=getattr(master, "on_site_since", None),
            avatar_path=getattr(master, "avatar_path", "static/default_avatar.png"),
        ),
    )

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Не удалось обновить мастера")

    return updated


