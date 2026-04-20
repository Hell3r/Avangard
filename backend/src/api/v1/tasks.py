from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from src.schemas.tasks import Task, TaskCreate, TaskUpdate, TaskComplete
from src.dependencies.services import TaskServiceDep
from src.dependencies.auth import ManagerOrAdminUser
from src.database.deps import SessionDep
from src.core.cache import cached
from src.services.RedisService import redis_service

router = APIRouter(prefix="/v1/tasks", tags=["Задачи"])

@router.get("/", response_model=List[Task], summary="Получить все задачи")
@cached(ttl=300)
async def get_tasks(service: TaskServiceDep, skip: int = 0, limit: int = 100):
    """
    Получить список всех задач с пагинацией.
    """
    return await service.get_all(skip, limit)

@router.get("/{task_id}", response_model=Task, summary="Получить задачу по ID")
async def get_task(task_id: int, service: TaskServiceDep):
    """
    Получить конкретную задачу по ID.
    """
    task = await service.get_by_id(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return task

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Создать задачу")
async def create_task(task_data: TaskCreate, service: TaskServiceDep, current_user: ManagerOrAdminUser):
    """
    Создать новую задачу. Только admin или manager.
    """
    await redis_service.delete_pattern("*tasks:*")
    return await service.create(task_data, current_user.id)

@router.put("/{task_id}", response_model=Task, summary="Обновить задачу")
async def update_task(task_id: int, task_data: TaskUpdate, service: TaskServiceDep, current_user: ManagerOrAdminUser):
    """
    Обновить задачу. Только admin или manager.
    """
    updated = await service.update(task_id, task_data)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return updated

@router.post("/{task_id}/complete", response_model=Task, summary="Завершить задачу")
async def complete_task(task_id: int, complete_data: TaskComplete, service: TaskServiceDep):
    """
    Завершить задачу.
    """
    completed = await service.complete(task_id, complete_data)
    if not completed:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")
    return completed

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Удалить задачу")
async def delete_task(task_id: int, service: TaskServiceDep, current_user: ManagerOrAdminUser):
    """
    Удалить задачу. Только admin или manager.
    """
    deleted = await service.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

