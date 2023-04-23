from sqlalchemy import insert, select

from conftest import client
from auth.models import Task, User
from conftest import async_session_maker


async def test_add_task():
    async with async_session_maker() as session:
        stmt = insert(Task).values(title='test_title', description='test_description', is_active=True)
        await session.execute(stmt)
        await session.commit()

        stmt2 = insert(Task).values(title='test_title2', description='test_description2', is_active=True)
        await session.execute(stmt2)
        await session.commit()

        query = select(Task.task_id, Task.title)
        result = await session.execute(query)
        assert result.all() == [(1, 'test_title'), (2, 'test_title2')], 'error'
