from uuid import UUID

from datetime import datetime
from pydantic.main import BaseModel


class TaskSchema(BaseModel):
    task_id: int
    title: str
    description: str
    is_active: bool
    user_id: UUID

    class Config:
        orm_mode = True
