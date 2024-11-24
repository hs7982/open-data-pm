from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import get_db
from service.getData import GetData

data_router = APIRouter(
    prefix="/api/data",
    tags=["미세먼지 데이터"],
)

@data_router.get('')
async def get_data(
    latitude: float = Query(..., description="위도"),
    longitude: float = Query(..., description="경도"),
    radius: int = Query(10000, description="검색 반경(미터)"),
    db: AsyncSession = Depends(get_db)
):
    """
    지정된 위치 주변의 대기오염 데이터를 조회합니다.
    
    Args:
        latitude (float): 위도
        longitude (float): 경도
        radius (int): 검색 반경(미터)
    """
    return await GetData.getDataByRadius(db, latitude, longitude, radius)