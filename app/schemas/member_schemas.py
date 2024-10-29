import uuid
from pydantic import (
    BaseModel,
    EmailStr,
    Field
)

from app.schemas import Gender


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
