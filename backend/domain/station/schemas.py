from typing import Optional
from geoalchemy2 import WKTElement
from pydantic import BaseModel


class StationBase(BaseModel):
    station_name: str  # 측정소명
    addr: Optional[str] = None  # 주소
    installation_year: Optional[int] = None  # 설치년도
    mang_name: Optional[str] = None  # 측정망 이름
    items: Optional[str] = None  # 측정 항목들

    class Config:
        arbitrary_types_allowed = True  # WKTElement 타입 허용


class StationCreate(StationBase):
    location: WKTElement  # 위치: WGS84 좌표 (문자열로 받기)

    class Config:
        arbitrary_types_allowed = True  # WKTElement 타입 허용


class Station(StationBase):
    station_code: str  # 측정소 코드 (기본 키)
    location: WKTElement  # 위치 (WGS84 좌표)

    class Config:
        orm_mode = True  # ORM 모델을 사용하여 데이터 변환
        arbitrary_types_allowed = True  # WKTElement 타입 허용
