from fastapi import APIRouter, HTTPException, status, Depends
from src.database.deps import SessionDep
from src.schemas.storage import Storage, StorageCreate, StorageUpdate
from src.dependencies.services import StorageServiceDep
from typing import List
from src.dependencies.auth import AdminUser
from src.core.cache import cached
from src.services.RedisService import redis_service

router = APIRouter(prefix="/v1/storage", tags=["Склад"])


@router.get("/", response_model=List[Storage], summary="Получить все материалы")
@cached(ttl = 300)
async def get_storages(service: StorageServiceDep, skip: int = 0, limit: int = 100):
    """
    Получить список всех материалов на складе с пагинацией.
    """
    return await service.get_all(skip, limit)

@router.get("/{storage_id}", response_model=Storage, summary="Получить материал по ID")
async def get_storage(storage_id: int, service: StorageServiceDep):
    """
    Получить конкретный материал по его ID.
    """
    storage = await service.get_by_id(storage_id)
    if not storage:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Материал не найден")
    return storage

@router.post("/", response_model=Storage, status_code=status.HTTP_201_CREATED, summary="Создать материал")
async def create_storage(storage_data: StorageCreate, service: StorageServiceDep, current_admin: AdminUser):
    """
    Создать новый материал на складе. Только admin.
    """
    await redis_service.delete_pattern("*storage:*")
    return await service.create(storage_data, actor_user_id=current_admin.id)


@router.put("/{storage_id}", response_model=Storage, summary="Обновить материал")
async def update_storage(storage_id: int, storage_data: StorageUpdate, service: StorageServiceDep, current_admin: AdminUser):
    """
    Обновить существующий материал. Только admin.
    """
    updated = await service.update(storage_id, storage_data, actor_user_id=current_admin.id)

    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Материал не найден")
    return updated

@router.delete("/{storage_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить материал")
async def delete_storage(storage_id: int, service: StorageServiceDep, current_admin: AdminUser):
    """
    Удалить материал по ID. Только admin.
    """
    deleted = await service.delete(storage_id, actor_user_id=current_admin.id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Материал не найден")

