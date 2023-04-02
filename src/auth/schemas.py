from pydantic.main import BaseModel

from task.schemas import TaskSchema
import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    id: uuid.UUID
    username: str
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool

    # tasks: list[TaskSchema]
    class Config:
        orm_mode = True
        exclude = {"tasks"}


class UserCreate(schemas.BaseUserCreate):
    username: str

