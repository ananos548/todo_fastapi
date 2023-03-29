from datetime import datetime
from enum import Enum

from pydantic import Field, EmailStr
from pydantic.main import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    password: str


class Task(BaseModel):
    title: str = Field(max_length=255)
    description: str | None = None
    price: float = Field(ge=0)
    like: bool | None = False
