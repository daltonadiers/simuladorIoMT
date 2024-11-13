import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import logging

LOG = logging.getLogger(__name__)

if os.getenv("ENVIRONMENT") == "production":
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASS = os.getenv("DB_PASS")
    DB_NAME = os.getenv("DB_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@/{DB_NAME}?host=/cloudsql/{INSTANCE_CONNECTION_NAME}"
else:
    load_dotenv()
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def connect_db() -> Session:
    try:
        db_session = SessionLocal()
        LOG.info("Connected to DB!")
        return db_session
    except Exception as e:
        LOG.error(f"Error connecting to DB: {e}")
        return

def close_db(db_session: Session):
    LOG.info("Closed to DB!")
    db_session.close()