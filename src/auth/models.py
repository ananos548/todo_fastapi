from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, Boolean, Integer
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

Base = declarative_base()


class Task(Base):
    __tablename__ = "task"

    task_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    is_active = Column(Boolean(), default=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="tasks")


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(255), nullable=False)
    email = Column(String(254), unique=True, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    tasks = relationship(Task, back_populates="user")
    hashed_password = Column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
