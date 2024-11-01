from fastapi import (
    APIRouter,
    Body,
    status,
    UploadFile,
    Depends,
    HTTPException,
    Query,
    Path,
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
    MatchAlreadyExistError,
    MatchLimitReachedError,
)
from app.schemas import (
    MemberCreateForm,
    MemberFromDB,
    MemberLogin,
    Payload,
    Gender,
    OrderBy,
    Distance,
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
        client_service: Annotated[
            ClientService,
            Depends(get_client_service(db.get_session)),
        ],
        name: str | None = Query(default=None),
        surname: str | None = Query(default=None),
        order_by: OrderBy | None = Query(default=None),
        distance: Distance | None = Query(default=None),
        gender: Gender | None = Query(default=None),
) -> list[MemberFromDB] | None:
    members = await client_service.get_members_list(
        for_subject=payload.sub,
        gender=gender,
        name=name,
        surname=surname,
        order_by=order_by,
        distance=distance,
    )
    return members


@router.post(
    path="/{member_id}/match",
    status_code=status.HTTP_200_OK,
    description="Endpoint to match member",
)
async def match_member(
        payload: Annotated[
            Payload,
            Depends(get_token_payload)
        ],
        client_service: Annotated[
            ClientService,
            Depends(get_client_service(db.get_session)),
        ],
        member_id: Annotated[int, Path()],
) -> JSONResponse:
    try:
        email = await client_service.match_member(
            from_member=payload.sub,
            with_member=member_id,
        )
        response_content = dict(message="Successfully matched")
        if email:
            response_content.update(
                email=email,
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=response_content,
        )
    except MatchAlreadyExistError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Can't match member twice",
        )
    except MatchLimitReachedError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limit of matches per day reached",
        )
