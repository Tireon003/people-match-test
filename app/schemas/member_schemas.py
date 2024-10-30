import uuid

from fastapi import Form
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from app.schemas import Gender, OrderBy


class BaseMember(BaseModel):
    email: EmailStr = Field(
        min_length=5,
        max_length=64,
    )
    name: str = Field(
        min_length=2,
        max_length=64,
    )
    surname: str = Field(
        min_length=2,
        max_length=64,
    )
    gender: Gender
    lat: float = Field(
        gt=-90,
        lt=90,
    )
    lon: float = Field(
        gt=-180,
        lt=180,
    )


class MemberCreateForm(BaseMember):
    password: str = Field(
        min_length=8,
    )

    @classmethod
    def as_form(
            cls,
            email: str = Form(...),
            name: str = Form(...),
            surname: str = Form(...),
            gender: str = Form(...),
            lat: float = Form(...),
            lon: float = Form(...),
            password: str = Form(...),
    ) -> "MemberCreateForm":
        return cls(
            email=email,
            name=name,
            surname=surname,
            gender=gender,
            lat=lat,
            lon=lon,
            password=password
        )


class MemberCreateSchema(BaseMember):
    hashed_password: str
    avatar: uuid.UUID


class MemberFromDB(MemberCreateSchema):
    id: int

    class Config:
        from_attributes = True


class MemberLogin(BaseModel):
    email: EmailStr = Field(
        min_length=5,
        max_length=64,
    )
    password: str = Field(
        min_length=8,
    )


class MembersFilter(BaseModel):
    gender: Gender | None = Field(default=None)
    name: str | None = Field(
        min_length=2,
        max_length=64,
        default=None,
    )
    surname: str | None = Field(
        min_length=2,
        max_length=64,
        default=None,
    )
    order_by: OrderBy | None = Field(default=None)
