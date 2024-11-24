from sqlalchemy.ext.asyncio import AsyncSession
from utils.sql_loader import load_sql_query
from sqlalchemy import text


class GetData:
    @staticmethod
    async def getDataByRadius(db: AsyncSession, latitude: float, longitude: float, radius: int = 20000):
        query = load_sql_query('pollution_queries.sql')
        result = await db.execute(
            text(query),
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius
            }
        )
        return result.mappings().all()