from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine
import logging
from config import DATABASE_URL

LOG = logging.getLogger(__name__)
    
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    with Session(engine) as db:
        yield db