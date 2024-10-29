from sqlalchemy import (
    String,
    LargeBinary,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from enum import Enum

from .base import Base


class Gender(Enum):
    male: str = 'male'
    female: str = 'female'


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
    avatar: Mapped[LargeBinary]
    hashed_password: Mapped[str] = mapped_column(
        nullable=False,
    )
