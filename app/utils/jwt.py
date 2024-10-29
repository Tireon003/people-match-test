import jwt
from datetime import (
    datetime as dt,
    timezone,
)

from app.exceptions import ExpiredTokenException
from app.schemas import Payload


class JwtTool:

    ALG: str = 'HS256'
    SECRET: str = '4qn9j23yb56b5n5nd3g54f43f'  # fixme get from env

    @classmethod
    def generate(cls, payload: Payload) -> str:
        return jwt.encode(
            payload=payload.model_dump(),
            key=cls.SECRET,
            algorithm=cls.ALG,
        )

    @classmethod
    def validate(cls, token: str) -> Payload:
        payload = jwt.decode(
            jwt=token,
            key=cls.SECRET,
            algorithms=[cls.ALG]
        )
        if dt.now(tz=timezone.utc) > payload['exp']:
            raise ExpiredTokenException()
        else:
            return Payload(**payload)
