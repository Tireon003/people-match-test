from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    ForeignKey,
)

from .base import Base


class MatchesORM(Base):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        nullable=False,
    )
    from_member: Mapped[int] = mapped_column(
        ForeignKey(
            'members.id',
            ondelete="CASCADE",
        ),
        index=True,
    )
    with_member: Mapped[int] = mapped_column(
        ForeignKey(
            'members.id',
            ondelete="CASCADE",
        ),
        index=True,
    )
