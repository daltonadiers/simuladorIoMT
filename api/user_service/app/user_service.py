from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from sqlalchemy.orm import Session
from models import UserInput, TypeOutput 
from database import *
from user_actions import *
from typing import List


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

@app.get("/users/")
async def get_users():
    result = get_user(db_session)
    return result
    
@app.get("/users/{seq}")
async def get_users_by_id(seq: int):
    result = get_user(db_session, seq)
    return result

@app.post("/users/")
async def post_users(data: UserInput):
    result = post_user(db_session, data)
    return result


@app.put("/users/{seq}")
async def put_users(seq:int, data: UserInput):
    result = put_user(db_session, data, seq)
    return result

@app.delete("/users/{seq}")
async def delete_users(seq:int):
    result = delete_user(db_session, seq)
    return result

@app.get("/users/{seq}/types/", response_model=List[TypeOutput])
async def get_user_types(seq: int):
    types = get_types_by_user(db_session, seq)
    return types

@app.delete("/users/{seq_user}/types/{type}")
async def delete_user_types(seq_user: int, type: int):
    types = delete_types_by_user(db_session, seq_user, type)
    return types
