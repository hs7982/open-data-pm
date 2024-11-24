import httpx
from decouple import config
from geoalchemy2 import WKTElement
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import json

from domain import Pollution
from domain.station.entities import Station


class APIReq:
    @staticmethod
    async def get(type: str, db: AsyncSession):
        API_KEY = config('OPEN_API_KEY')
        API_RETURN_TYPE = 'json'
        API_SIDO = '전국'

        if type == "pollution":
            print("#### 미세먼지 데이터 추가 시작")
            url = f'https://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey={API_KEY}&returnType={API_RETURN_TYPE}&numOfRows=1000&pageNo=1&sidoName={API_SIDO}&ver=1.5'
        elif type == "station":
            print("#### 측정소 데이터 추가 시작")
            url = f'https://apis.data.go.kr/B552584/MsrstnInfoInqireSvc/getMsrstnList?serviceKey={API_KEY}&returnType={API_RETURN_TYPE}&numOfRows=1000&pageNo=1&sidoName={API_SIDO}&ver=1.1'
        else:
            raise Exception("잘못된 type입니다.")

        try:
            res = httpx.get(url, timeout=15)
            res.raise_for_status()
            data = res.json()  # 메서드 호출 필

            if type == "pollution":
                await APIReq.save_pollution_data(data, db)
            elif type == "station":
                await APIReq.save_station_data(data, db)

            return {"message": f"{type} 데이터가 성공적으로 저장되었습니다."}

        except httpx.RequestError as e:
            raise Exception(f"API요청 중 오류가 발생하였습니다: {e}")
        except httpx.HTTPStatusError as e:
            raise Exception(f"API요청 중 상태코드 오류가 발행하였습니다: {e}")

    @staticmethod
    async def save_station_data(data: dict, db: AsyncSession):
        try:

            if isinstance(data, str):
                data = json.loads(data)
            
            station_list = data.get("response", {}).get("body", {}).get("items", [])
            append_data=0
            for entry in station_list:
                year = entry.get('year')
                installation_year = int(year) if year and year.isdigit() else None

                stmt = select(Station).where(Station.station_code == entry.get('stationCode'))
                result = await db.execute(stmt)
                existing_station = result.scalar_one_or_none()

                if existing_station:
                    continue
                append_data += 1
                station = Station(
                    station_code=entry.get('stationCode'),
                    station_name=entry.get('stationName'),
                    addr=entry.get('addr'),
                    installation_year=installation_year,
                    mang_name=entry.get('mangName'),
                    items=entry.get('item'),
                    location=WKTElement(
                        f"POINT({entry.get('dmX')} {entry.get('dmY')})",
                        srid=4326
                    )
                )
                db.add(station)
            
            await db.commit()
            print("추가된 측정소 데이터: ",append_data,"개")
            
        except Exception as e:
            await db.rollback()
            raise Exception(f"Error saving station data: {str(e)}")

    @staticmethod
    async def save_pollution_data(data: dict, db: AsyncSession):
        try:
            if isinstance(data, str):
                data = json.loads(data)
            pollution_list = data.get("response", {}).get("body", {}).get("items", [])

            def convert_value(value, t=None):
                if value is None or value == "-":
                    return None
                return int(value) if t == int else float(value)
            append_data = 0
            for entry in pollution_list:
                from datetime import datetime
                data_time_str = entry.get('dataTime')
                data_time = datetime.strptime(data_time_str, '%Y-%m-%d %H:%M') if data_time_str else None

                stmt = select(Pollution).where(
                    Pollution.station_code == entry.get('stationCode'),
                    Pollution.data_time == data_time
                )
                result = await db.execute(stmt)
                existing_pollution = result.scalar_one_or_none()
                
                if existing_pollution:
                    continue
                append_data += 1

                pollution = Pollution(
                    station_code=entry.get('stationCode'),
                    data_time=data_time,
                    so2_value=convert_value(entry.get('so2Value')),
                    co_value=convert_value(entry.get('coValue')),
                    o3_value=convert_value(entry.get('o3Value')),
                    no2_value=convert_value(entry.get('no2Value')),
                    pm10_value=convert_value(entry.get('pm10Value'), int),
                    pm2_5_value=convert_value(entry.get('pm25Value'), int),
                    so2_flag=entry.get('so2Flag'),
                    co_flag=entry.get('coFlag'),
                    o3_flag=entry.get('o3Flag'),
                    no2_flag=entry.get('no2Flag'),
                    pm10_flag=entry.get('pm10Flag'),
                    pm2_5_flag=entry.get('pm25Flag'),
                    so2_grade=entry.get('so2Grade'),
                    co_grade=entry.get('coGrade'),
                    o3_grade=entry.get('o3Grade'),
                    no2_grade=entry.get('no2Grade'),
                    pm10_grade=entry.get('pm10Grade'),
                    pm2_5_grade=entry.get('pm25Grade'),
                    khai_value=entry.get('khaiValue'),
                    khai_grade=entry.get('khaiGrade')
                )
                db.add(pollution)

            await db.commit()
            print("추가된 미세먼지 데이터: ",append_data,"개")

        except Exception as e:
            await db.rollback()
            raise Exception(f"Error saving pollution data: {str(e)}")