from fastapi import FastAPI

from schemas.base import *

app = FastAPI()


@app.get('/users/', response_model=list[User])
async def get_user(user: User):
    return user


@app.post('/tasks/')
async def create_task(task: Task):
    return task
