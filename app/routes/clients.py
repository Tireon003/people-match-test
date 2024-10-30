import json

from fastapi import (
    APIRouter,
    Body,
    status,
    UploadFile,
    Depends,
    HTTPException,
    Form,
)
from fastapi.responses import (
    JSONResponse,
)
from typing import Annotated

from app.exceptions import (
    BadImageProvidedError,
    MemberNotFoundException,
    WrongPasswordException,
    EmailAlreadyUsedError,
)
from app.schemas import (
    MemberCreateForm,
    MembersFilter,
    MemberFromDB,
    MemberLogin,
    Payload,
)
from app.dependencies import (
    get_client_service,
    get_token_payload,
)
from app.core import db
from app.services import ClientService


router: APIRouter = APIRouter(
    prefix="/api/clients",
    tags=["Clients"],
)


@router.post(
    path="/create",
    status_code=status.HTTP_201_CREATED,
    response_model=MemberFromDB,
    description="Endpoint to create a new member",
)
async def create_new_member(
        member_create_form: Annotated[
            MemberCreateForm,
            Depends(MemberCreateForm.as_form)
        ],
        member_input_avatar: UploadFile,
        client_service: Annotated[
            ClientService,
            Depends(get_client_service(db.get_session)),
        ],
) -> MemberFromDB:
    try:
        new_member = await client_service.create_member(
            member_data=member_create_form,
            member_avatar=member_input_avatar,
        )
        return new_member
    except BadImageProvidedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.info,
        )
    except EmailAlreadyUsedError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email: {e.email} already exists",
        )


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    description="Endpoint to log in member",
)
async def login_member(
        login_data: Annotated[MemberLogin, Body()],
        client_service: Annotated[
            ClientService,
            Depends(get_client_service(db.get_session)),
        ],
) -> JSONResponse:
    try:
        token = await client_service.authenticate_member(login_data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=dict(
                access_token=token,
                token_type="Bearer",
            )
        )
    except MemberNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Member not found",
        )
    except WrongPasswordException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong password",
            headers={
                "WWW-Authenticate": "Bearer",
            }
        )


@router.get(
    path="/list",
    status_code=status.HTTP_200_OK,
    response_model=list[MemberFromDB],
    description="Endpoint to get members list"
)
async def get_members_list(
        payload: Annotated[
            Payload,
            Depends(get_token_payload)
        ],
        members_filter: Annotated[
            MembersFilter,
            Body()
        ],
        client_service: Annotated[
            ClientService,
            Depends(get_client_service(db.get_session)),
        ],
) -> list[MemberFromDB] | None:
    members = await client_service.get_members_list(
        exclude_member=payload.sub,
        filters=members_filter,
    )
    return members
