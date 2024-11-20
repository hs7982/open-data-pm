from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from typing import Optional
from datetime import datetime

from core.db_base import Base

class Pollution(Base):
    __tablename__ = "pollution"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    station_code: Mapped[str] = mapped_column(String(6), ForeignKey("stations.station_code"), nullable=False)
    data_time: Mapped[datetime] = mapped_column(DateTime)

    #value
    so2_value: Mapped[Optional[float]] = mapped_column(Float)
    co_value: Mapped[Optional[float]] = mapped_column(Float)
    o3_value: Mapped[Optional[float]] = mapped_column(Float)
    no2_value: Mapped[Optional[float]] = mapped_column(Float)
    pm10_value: Mapped[Optional[int]] = mapped_column(Integer)
    pm2_5_value: Mapped[Optional[int]] = mapped_column(Integer)

    #flag
    so2_flag: Mapped[Optional[str]] = mapped_column(String(10))
    co_flag: Mapped[Optional[str]] = mapped_column(String(10))
    o3_flag: Mapped[Optional[str]] = mapped_column(String(10))
    no2_flag: Mapped[Optional[str]] = mapped_column(String(10))
    pm10_flag: Mapped[Optional[str]] = mapped_column(String(10))
    pm2_5_flag: Mapped[Optional[str]] = mapped_column(String(10))

    #grade
    so2_grade: Mapped[Optional[str]] = mapped_column(String(10))
    co_grade: Mapped[Optional[str]] = mapped_column(String(10))
    o3_grade: Mapped[Optional[str]] = mapped_column(String(10))
    no2_grade: Mapped[Optional[str]] = mapped_column(String(10))
    pm10_grade: Mapped[Optional[str]] = mapped_column(String(10))
    pm2_5_grade: Mapped[Optional[str]] = mapped_column(String(10))

    #khai
    khai_value: Mapped[Optional[str]] = mapped_column(String(10))
    khai_grade: Mapped[Optional[str]] = mapped_column(String(10))

    station: Mapped["Station"] = relationship(back_populates="pollution")


