from fastapi import (
    FastAPI,
    Request,
    status,
)

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError

from app.routes import clients_router


app = FastAPI(
    redoc_url=None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # fixme get from env variables
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
