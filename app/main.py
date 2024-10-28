from fastapi import (
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware


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

