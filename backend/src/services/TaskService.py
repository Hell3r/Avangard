from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.tasks import TaskModel
from src.schemas.tasks import TaskCreate, TaskUpdate, TaskComplete
from typing import Optional, List


class TaskService:

    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        result = await self.session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .offset(skip)
            .limit(limit)
            .order_by(TaskModel.id)
        )
        return result.scalars().all()
    
async def create(self, task_data: TaskCreate, current_user_id: int) -> TaskModel:
    db_task = TaskModel(
        assigned_by_id=current_user_id,
        **task_data.dict(exclude={"assigned_by_id"})
    )
    self.session.add(db_task)
    await self.session.commit()
    await self.session.refresh(db_task)
    return db_task
    
    async def update(self, task_id: int, task_data: TaskUpdate) -> Optional[TaskModel]:
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        update_data = task_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)
        
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def complete(self, task_id: int, complete_data: TaskComplete) -> Optional[TaskModel]:
        task = await self.get_by_id(task_id)
        if not task:
            return None
        
        task.completed_at = complete_data.completed_at
        await self.session.commit()
        await self.session.refresh(task)
        return task
    
    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        return False
