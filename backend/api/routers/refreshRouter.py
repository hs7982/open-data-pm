from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db
from service.APIReq import APIReq

refresh_router = APIRouter(
    prefix="/api/refresh",
    tags=["API 데이터 갱신"],
)

@refresh_router.get('/data',
    summary="대기오염 데이터 갱신",
    description="OPEN API에서 최신 대기오염 측정 데이터를 가져와 반영합니다.",
    response_description="처리결과"
)
async def get_data(db: Session = Depends(get_db)):
    return await APIReq.get("pollution", db)

@refresh_router.get('/station',
    summary="측정소 정보 갱신",
    description="OPEN API에서 측정소 정보를 가져와 반영합니다.",
    response_description="처리결과",
)
async def get_data(db: Session = Depends(get_db)):
    return await APIReq.get("station", db)