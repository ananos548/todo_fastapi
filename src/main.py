import uuid
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend

from auth.manager import get_user_manager
from auth.schemas import UserRead, UserCreate
from auth.models import User
from task.router import router as router_task

app = FastAPI()

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

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

current_user = fastapi_users.current_user()


app.include_router(router_task)