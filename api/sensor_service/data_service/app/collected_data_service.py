from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from sqlalchemy.orm import Session

from collected_data_actions import *
from database import *
from models import CollectedDataInput

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

db_session: Session

@asynccontextmanager
async def lifespan(app: FastAPI):
    global db_session
    try:
        db_session = connect_db()
        yield
    except:
        raise SystemExit("Critical error!")
    finally:
        close_db(db_session)

app = FastAPI(lifespan=lifespan)

@app.get("/collected-data/")
async def get_collected_data():
    result = get_data(db_session)
    return result

@app.get("/collected-data/{seq}")
async def get_collected_data_by_seq(seq: int):
    result = get_data(db_session, seq)
    return result

@app.get("/collected-data/user/{id}")
async def get_collected_dataUser_by_id(id: int):
    result = get_dataUser(db_session, id)
    return result

@app.get("/collected-data/user/{id}/{type}")
async def get_collected_dataUser_by_id(id: int, type: int):
    result = get_dataUser(db_session, id, type)
    return result

@app.post("/collected-data/")
async def post_collected_data(data: CollectedDataInput):
    result = post_data(db_session, data)
    return result

@app.put("/collected-data/{seq}")
async def update_collected_data(seq: int, data: CollectedDataInput):
    result = put_data(db_session, data, seq)
    return result

@app.delete("/collected-data/{seq}")
async def delete_collected_data(seq: int):
    result = delete_data(db_session, seq)
    return result
