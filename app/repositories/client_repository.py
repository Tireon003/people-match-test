from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    select,
    desc,
)
from typing import Sequence

from app.models import MembersORM
from app.schemas import (
    MemberCreateSchema,
    MembersFilter,
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
            filter_schema: MembersFilter,
            exclude_member: int,
    ) -> Sequence[MembersORM]:
        stmt = (
            select(MembersORM)
            .filter(MembersORM.id != exclude_member)
        )
        if filter_schema.gender:
            stmt = stmt.filter_by(gender=filter_schema.gender)
        if filter_schema.name:
            stmt = stmt.filter_by(name=filter_schema.name)
        if filter_schema.surname:
            stmt = stmt.filter_by(surname=filter_schema.surname)
        if filter_schema.order_by:
            stmt = stmt.order_by(desc(MembersORM.id))
        result = await self.__session.scalars(stmt)
        return result.all()
