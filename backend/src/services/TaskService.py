from __future__ import annotations

import asyncio
from datetime import datetime, timedelta
from typing import Optional, List, Callable, Awaitable

from sqlalchemy import select, update, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.tasks import TaskModel
from src.schemas.tasks import Task
from src.schemas.tasks import TaskCreate, TaskUpdate, TaskComplete
from src.services.EventJournalService import EventJournalService



class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        result = await self.session.execute(
            select(TaskModel)
            .options(joinedload(TaskModel.assigned_to))
            .where(TaskModel.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Task]:
        result = await self.session.execute(
            select(TaskModel)
            .options(joinedload(TaskModel.assigned_to))
            .offset(skip)
            .limit(limit)
            .order_by(TaskModel.id)
        )

        tasks = result.scalars().all()
        return [Task.model_validate(t, from_attributes=True) for t in tasks]

    async def create(self, task_data: TaskCreate, current_user_id: int) -> TaskModel:
        db_task = TaskModel(
            assigned_by_id=current_user_id,
            **task_data.model_dump(exclude={"assigned_by_id"}),
        )
        self.session.add(db_task)
        await self.session.commit()
        await self.session.refresh(db_task)

        # чтобы pydantic не лез в lazy relationship и не словил MissingGreenlet
        await self.session.refresh(db_task, attribute_names=["assigned_to"])

        await EventJournalService(self.session).log_event(
            f"task_created; task_id={db_task.id}; actor_user_id={current_user_id}; assigned_to_id={db_task.assigned_to_id}; due_at={db_task.due_at}; status={db_task.status}"
        )

        return db_task



    async def update(self, task_id: int, task_data: TaskUpdate) -> Optional[TaskModel]:
        task = await self.get_by_id(task_id)
        if not task:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.session.commit()
        await self.session.refresh(task)
        
        return task

    async def complete(

        self,
        task_id: int,
        complete_data: TaskComplete,
        actor_user_id: Optional[int] = None,
    ) -> Optional[TaskModel]:
        task = await self.get_by_id(task_id)
        if not task:
            return None

        task.completed_at = complete_data.completed_at
        await self.session.commit()
        await self.session.refresh(task)

        await EventJournalService(self.session).log_event(
            f"Задача завершена; Название задачи={task.description};"
        )

        return task


    async def delete(self, task_id: int) -> bool:

        task = await self.get_by_id(task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
            return True
        return False

    @staticmethod
    async def update_overdue_status(session_factory: Callable[[], Awaitable[AsyncSession]]):
        async with (await session_factory) as session:
            now = func.now()

            await session.execute(
                update(TaskModel)
                .where(
                    and_(
                        TaskModel.completed_at.is_(None),
                        TaskModel.due_at.is_not(None),
                        TaskModel.due_at < now,
                    )
                )
                .values(status="Просрочено")
            )

            await session.execute(
                update(TaskModel)
                .where(
                    and_(
                        TaskModel.completed_at.is_(None),
                        TaskModel.due_at.is_not(None),
                        TaskModel.due_at >= now,
                        TaskModel.status == "Просрочено",
                    )
                )
                .values(status="В работе")
            )

            await session.commit()

    @staticmethod
    async def overdue_updater_loop(
        session_factory: Callable[[], Awaitable[AsyncSession]],
        interval_seconds: int = 24 * 60 * 60,
    ):
        # Сначала применяем сразу при старте
        while True:
            try:
                await TaskService.update_overdue_status(session_factory)
            except Exception:
                # намеренно глушим, чтобы цикл не падал
                pass
            await asyncio.sleep(interval_seconds)


