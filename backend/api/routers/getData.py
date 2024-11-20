from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from service.APIReq import APIReq

getData_Router = APIRouter()

@getData_Router.get('/getData')
async def get_data(db: Session = Depends(get_db)):
    return await APIReq.get("pollution", db)

@getData_Router.get('/getStation')
async def get_data(db: Session = Depends(get_db)):
    return await APIReq.get("station", db)