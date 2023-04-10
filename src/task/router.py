from sqlalchemy import select, insert, orm, update
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_async_session
from auth.models import Task, User

from task.schemas import TaskSchema
from utils import current_user

router = APIRouter(
    prefix='/tasks',
    tags=['Task']
)


@router.post('/')
async def add_tasks(new_task: TaskSchema, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(Task).values(**new_task.dict())
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}


@router.get('/user_tasks/')
async def get_user_tasks(user_id: UUID, user: User = Depends(current_user),
                         session: AsyncSession = Depends(get_async_session)):
    """get user tasks (for superuser only)"""
    if user.is_superuser is False:
        raise HTTPException(status_code=403, detail='Permission denied')
    query = select(Task).where(Task.user_id == user_id).options(
        orm.load_only(Task.title, Task.description, Task.user_id, Task.is_active)
    )
    result = await session.execute(query)
    tasks = result.scalars().all()
    return tasks


@router.get('/my_tasks')
async def get_my_tasks(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.user == user)
    result = await session.execute(query)
    tasks = result.scalars().all()
    return f"hello {user.username}, your tasks are :", tasks


@router.put('/change_active/{task_id}')
async def change_active(task_id: int, is_active: bool, user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    # check task
    task = await session.execute(select(Task).where(Task.user == user).where(Task.task_id == task_id))
    if not task.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"You haven't task with id {task_id}")

    # update is_active
    stmt = update(Task).where(Task.user == user).where(Task.task_id == task_id).values(is_active=is_active)
    await session.execute(stmt)
    await session.commit()

    # query to return is_active
    query_task = select(Task.is_active).where(Task.task_id == task_id)
    result = await session.execute(query_task)
    tasks_status = result.scalars().all()
    return {"status": status.HTTP_200_OK}, f"task status: {str(tasks_status)}"

