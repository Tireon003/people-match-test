from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    desc,
)
from typing import Sequence

from app.models import MembersORM
from app.schemas import (
    MemberCreateSchema,
    MembersFilter, Coordinates, Gender, OrderBy,
)


class ClientRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def select_member_by_email(self, email: str) -> MembersORM | None:
        stmt = (
            select(MembersORM)
            .filter_by(email=email)
        )
        result = await self.__session.scalars(stmt)
        return result.one_or_none()

    async def insert_member(
            self,
            member: MemberCreateSchema
    ) -> MembersORM:
        member_orm = MembersORM(**member.model_dump())
        self.__session.add(member_orm)
        await self.__session.flush()
        await self.__session.refresh(member_orm)
        await self.__session.commit()
        return member_orm

    async def select_members(
            self,
            gender: Gender | None = None,
            name: str | None = None,
            surname: str | None = None,
            order_by: OrderBy | None = None,
    ) -> Sequence[MembersORM]:
        stmt = (
            select(MembersORM)
        )
        if gender:
            stmt = stmt.filter_by(gender=gender)
        if name:
            stmt = stmt.filter_by(name=name)
        if surname:
            stmt = stmt.filter_by(surname=surname)
        if order_by:
            if order_by == OrderBy.reg_date:
                stmt = stmt.order_by(desc(MembersORM.id))
        result = await self.__session.scalars(stmt)
        return result.all()

    async def select_member(self, member_id: int) -> MembersORM | None:
        member = await self.__session.get(MembersORM, member_id)
        return member
