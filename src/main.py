from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.base_config import auth_backend

from auth.schemas import UserRead, UserCreate
from auth.models import User, Task
from database import get_async_session
from task.router import router as router_task
from utils import fastapi_users, current_user

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_task)
