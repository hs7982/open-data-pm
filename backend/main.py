from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.getData import getData_Router

from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
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

@app.get("/")
async def pingPong():
    return {"ping": "pong!"}
