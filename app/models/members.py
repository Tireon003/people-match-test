from sqlalchemy import (
    String,
    Float,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import Base

from app.schemas import (
    Gender,
)
import uuid


class MembersORM(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
    )
    gender: Mapped[Gender]
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    surname: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )
    avatar: Mapped[uuid.UUID]
    hashed_password: Mapped[str] = mapped_column(
        nullable=False,
    )
    lat: Mapped[float] = mapped_column(
        Float(4),
        nullable=False,
    )
    lon: Mapped[float] = mapped_column(
        Float(4),
        nullable=False,
    )
