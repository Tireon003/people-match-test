from fastapi import UploadFile

from app.exceptions import EmailAlreadyUsedError, WrongPasswordException, MemberNotFoundException
from app.repositories import ClientRepository
from app.schemas import (
    MemberCreateForm,
    MemberCreateSchema,
    MemberFromDB, MemberLogin, Payload, MembersFilter,
)
from app.utils import save_image_with_watermark, HashTool, JwtTool


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.__repo = repository

    async def create_member(
            self,
            member_data: MemberCreateForm,
            member_avatar: UploadFile,
    ) -> MemberFromDB:
        user_with_email = await self.__repo.select_member_by_email(
            email=member_data.email,
        )
        if user_with_email is not None:
            raise EmailAlreadyUsedError(member_data.email)
        else:
            image_uuid = save_image_with_watermark(
                image_file=member_avatar,
            )
            member_create_schema = MemberCreateSchema(
                **member_data.model_dump(exclude={'password'}),
                hashed_password=HashTool.hash_password(member_data.password),
                avatar=image_uuid,
            )
            member_orm = await self.__repo.insert_member(member_create_schema)
            member_db_schema = MemberFromDB.model_validate(member_orm)
            return member_db_schema

    async def authenticate_member(self, login_form: MemberLogin) -> str:
        member = await self.__repo.select_member_by_email(login_form.email)
        if not member:
            raise MemberNotFoundException()
        elif not HashTool.check_password(
                password=login_form.password,
                hashed_password=member.hashed_password,
        ):
            raise WrongPasswordException()
        else:
            payload = Payload(
                sub=member.id,
                email=member.email,
            )
            token = JwtTool.generate(payload)
            return token

    async def get_members_list(
            self,
            exclude_member: int,
            filters: MembersFilter,
    ) -> list[MemberFromDB] | None:
        members_orm_list = await self.__repo.select_members(
            filter_schema=filters,
            exclude_member=exclude_member,
        )
        members_list_schema = [
            MemberFromDB.model_validate(item) for item in members_orm_list
        ]
        return members_list_schema
