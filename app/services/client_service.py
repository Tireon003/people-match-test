from typing import cast
from redis import asyncio as aioredis
from fastapi import UploadFile

from app.config import settings
from app.exceptions import (
    EmailAlreadyUsedError,
    WrongPasswordException,
    MemberNotFoundException,
    MatchAlreadyExistError,
    MatchLimitReachedError,
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
    increment_matches,
)
from app.tasks import send_match_notification


class ClientService:

    def __init__(self, repository: ClientRepository):
        self.__repo = repository
        self.__redis = aioredis.from_url(settings.REDIS_URL)

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
                if member.id != for_subject
            ]
            if distance:
                members_list_schema = [
                    member for member in members_list_schema
                    if (
                        await calculate_distance(
                            subject_coords.lat,
                            subject_coords.lon,
                            member.lat,
                            member.lon,
                        ) < float(distance.value)
                    )
                ]
            return members_list_schema

    async def match_member(
            self,
            from_member: int,
            with_member: int,
    ) -> str | None:
        match = await self.__repo.select_match_by_members(
            from_member=from_member,
            with_member=with_member,
        )
        if match:
            raise MatchAlreadyExistError()
        else:
            limit_reached = await increment_matches(from_member)
            if limit_reached:
                raise MatchLimitReachedError()
            await self.__repo.insert_match(
                from_member=from_member,
                with_member=with_member,
            )
            mutual_match = await self.__repo.select_match_by_members(
                from_member=with_member,
                with_member=from_member,
            )
            if mutual_match is not None:
                from_member_orm = await self.__repo.select_member(from_member)
                with_member_orm = await self.__repo.select_member(with_member)

                send_match_notification.delay(
                    email=cast(str, from_member_orm.email),
                    matched_name=cast(str, with_member_orm.name),
                    matched_email=cast(str, with_member_orm.email),
                )
                send_match_notification.delay(
                    email=cast(str, with_member_orm.email),
                    matched_name=cast(str, from_member_orm.name),
                    matched_email=cast(str, from_member_orm.email),
                )

                email = cast(str, with_member_orm.email)
                return email
            return None
