from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers.getData import getData_Router

from core.database import get_db, create_db
import sqlalchemy

app = FastAPI(
    title="미세먼지 측정 서비스",
    description="미세먼지 데이터 수집 및 조회 API",
    version="1.0.0",
)

app.include_router(getData_Router)


origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



create_db()
@app.get("/")
async def pingPong():
    return {"ping": "pong!"}
