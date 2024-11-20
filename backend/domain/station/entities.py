from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from geoalchemy2 import Geography
from typing import Optional

from core.db_base import Base

class Station(Base):
    __tablename__ = "stations"
    
    station_code: Mapped[str] = mapped_column(String(10), primary_key=True)
    station_name: Mapped[str] = mapped_column(String(30), nullable=False)
    addr: Mapped[Optional[str]] = mapped_column(String(510))
    installation_year: Mapped[Optional[int]] = mapped_column(Integer)
    mang_name: Mapped[Optional[str]] = mapped_column(String(100))
    items: Mapped[Optional[str]] = mapped_column(String(255))
    location: Mapped[Optional[Geography]] = mapped_column(
        Geography(geometry_type='POINT', srid=4326)
    )

    pollution = relationship("Pollution")

    # def __init__(self, **kwargs):
    #     super().__init__()
    #     for key, value in kwargs.items():
    #         setattr(self, key, value)
    #
    # def __str__(self):
    #     return (
    #         f"Station("
    #         f"station_code='{self.station_code}', "
    #         f"station_name='{self.station_name}', "
    #         f"addr='{self.addr}', "
    #         f"installation_year={self.installation_year}, "
    #         f"mang_name='{self.mang_name}', "
    #         f"items='{self.items}', "
    #         f"location={self.location}"
    #         f")"
    #     )