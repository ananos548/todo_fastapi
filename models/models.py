import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Table, Column, String, Text, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    title_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean(), default=True)


class User(Base):
    __tablename__ = "users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    password = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime)
    task_id = Column(UUID(as_uuid=True), ForeignKey("tasks.title_id"))
