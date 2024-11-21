from sqlalchemy.orm import Session
from utils.sql_loader import load_sql_query
from sqlalchemy import text


class GetData:
    @staticmethod
    def getDataByRadius(db: Session, latitude: float, longitude: float, radius: int = 10000):
        query = load_sql_query('pollution_queries.sql')
        result = db.execute(
            text(query),
            {
                "latitude": latitude,
                "longitude": longitude,
                "radius": radius
            }
        )
        return result.mappings().all()