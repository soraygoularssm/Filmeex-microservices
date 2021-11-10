from fastapi import Depends, FastAPI, Header, HTTPException
from .packs import movies, series, crew

import uvicorn

app = FastAPI()

app.include_router(
    movies.router,
    prefix='/movies',
    tags=["movies"]
)

app.include_router(
    series.router,
    prefix='/series',
    tags=["series"]
)

app.include_router(
    crew.router,
    prefix='/crew',
    tags=["crew"]
)