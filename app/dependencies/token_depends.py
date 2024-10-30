from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.schemas import Payload
from app.utils import JwtTool

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/clients/login")


def get_token_payload(
        access_token: Annotated[
            str,
            Depends(oauth2_scheme)
        ],
) -> Payload:  # todo add user exists checking
    payload = JwtTool.validate(access_token)
    return payload
