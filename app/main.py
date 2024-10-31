from collections.abc import AsyncIterator

from fastapi import (
    FastAPI,
    Request,
    status,
)
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError

from app.config import settings
from app.routes import clients_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.REDIS_URL)
    FastAPICache.init(
        backend=RedisBackend(redis),
        prefix="fastapi-cache"
    )
    yield


app = FastAPI(
    lifespan=lifespan,
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(clients_router)


@app.exception_handler(ExpiredSignatureError)
async def handle_expired_token_exception(
        request: Request,
        exc: ExpiredSignatureError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=dict(
            detail="Provided token is expired"
        ),
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )
