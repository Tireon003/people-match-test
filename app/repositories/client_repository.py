from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import MembersORM
from app.schemas import MemberCreateSchema


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
