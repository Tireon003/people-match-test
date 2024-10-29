from typing import (
    Callable,
    TypeVar,
)
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import ClientRepository
from app.services import ClientService


def get_client_service(
        get_async_session: Callable[..., AsyncSession],
) -> Callable[..., ClientService]:
    def _get_client_service(
            session: AsyncSession = Depends(get_async_session)
    ) -> ClientService:
        user_repo = ClientRepository(session)
        return ClientService(user_repo)
    return _get_client_service
