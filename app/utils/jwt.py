import jwt

from app.config import settings
from app.schemas import Payload


class JwtTool:

    ALG: str = 'HS256'
    SECRET: str = settings.SECRET

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
            algorithms=[cls.ALG],
            options={
                'verify_signature': True,
                'verify_exp': 'verify_signature',
            }
        )
        return Payload(**payload)
