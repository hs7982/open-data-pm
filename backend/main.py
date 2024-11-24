from contextlib import asynccontextmanager
from time import sleep

from service.APIReq import APIReq
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from utils.scheduler import scheduler
from api.routers.dataRouter import data_router
from api.routers.refreshRouter import refresh_router
from core.database import create_db
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await create_db()
    await asyncio.sleep(3)
    scheduler.start()
    yield
    # Shutdown
    scheduler.shutdown()

app = FastAPI(
    title="미세먼지 측정 서비스",
    description="미세먼지 데이터 수집 및 조회 API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(refresh_router)
app.include_router(data_router)
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

@app.get("/")
async def pingPong():
    return {"ping": "pong!", "See":"/docs"}
