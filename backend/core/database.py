from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from decouple import config
from .db_base import Base

import domain.station.entities
import domain.pollution.entities

SQLALCHEMY_DATABASE_URL = config("DB_URL")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_db():
    print("###DB 초기화")
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise Exception
    finally:
        db.close()