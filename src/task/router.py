from sqlalchemy import select, insert

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas import UserRead
from database import get_async_session
from auth.models import Task, User
from task.schemas import TaskSchema

router = APIRouter(
    prefix='/tasks',
    tags=['Task']
)


@router.get('/')
async def get_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(Task)
    result = await session.execute(query)
    tasks = result.scalars().all()
    task_schemas = [TaskSchema.from_orm(task).dict() for task in tasks]
    return {"tasks": task_schemas}


@router.post('/')
async def add_tasks(new_task: TaskSchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Task).values(**new_task.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}
