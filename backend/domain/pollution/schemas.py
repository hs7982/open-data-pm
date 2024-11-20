from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PollutionBase(BaseModel):
    data_time: datetime  # 측정 시간
    so2_value: Optional[float] = None  # 아황산가스 농도
    co_value: Optional[float] = None   # 일산화탄소 농도
    o3_value: Optional[float] = None   # 오존 농도
    no2_value: Optional[float] = None  # 이산화질소 농도
    pm10_value: Optional[int] = None   # PM10 농도
    pm2_5_value: Optional[int] = None  # PM2.5 농도

class PollutionCreate(PollutionBase):
    station_code: str  # 외래키: 측정소 코드

class Pollution(PollutionBase):
    id: int  # 고유 ID
    station_code: str  # 외래키: 측정소 코드

    class Config:
        orm_mode = True  # ORM 모델을 사용하여 데이터 변환