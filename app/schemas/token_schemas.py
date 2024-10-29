from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from datetime import (
    datetime,
    timezone,
    timedelta
)


class Payload(BaseModel):
    sub: int
    email: EmailStr
    exp: datetime = Field(
        default=datetime.now(tz=timezone.utc) + timedelta(days=7),
    )
