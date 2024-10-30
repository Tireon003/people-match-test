from fastapi import UploadFile

from app.exceptions import (
    EmailAlreadyUsedError,
    WrongPasswordException,
    MemberNotFoundException,
)
from app.repositories import ClientRepository
from app.schemas import (
    MemberCreateForm,
    MemberCreateSchema,
    MemberFromDB,
    MemberLogin,
    Payload,
    Coordinates,
    Gender,
    OrderBy,
    Distance,
)
from app.utils import (
    save_image_with_watermark,
    HashTool,
    JwtTool,
    calculate_distance,
)


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
            for_subject: int,
            gender: Gender | None,
            name: str | None,
            surname: str | None,
            order_by: OrderBy | None,
            distance: Distance | None,
    ) -> list[MemberFromDB] | None:
        subject = await self.__repo.select_member(for_subject)
        if not subject:
            raise MemberNotFoundException()
        else:
            members_orm_list = await self.__repo.select_members(
                gender=gender,
                name=name,
                surname=surname,
                order_by=order_by,
            )
            subject_coords = Coordinates(
                lat=subject.lat,
                lon=subject.lon,
            )
            members_list_schema = [
                MemberFromDB.model_validate(member)
                for member in members_orm_list
                if (
                    member.id != for_subject and
                    calculate_distance(
                        subject_coords.lat,
                        subject_coords.lon,
                        member.lat,
                        member.lon,
                    ) < distance
                )
            ]
            return members_list_schema
