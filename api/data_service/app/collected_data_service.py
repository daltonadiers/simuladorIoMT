from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from sqlalchemy.orm import Session
from collected_data_actions import *
from database import get_db
from models import CollectedDataInput, Token
from security import get_logged_user

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

db_session: Session

@asynccontextmanager
async def lifespan(app: FastAPI):
        yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8081",
    "http://34.121.42.246",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/token', response_model=Token)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
     token = get_login(db_session, form_data.username, form_data.password)
     return token

@app.get("/collected-data/")
async def get_collected_data(db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_data(db_session, logged_user)
    return result

@app.get("/collected-data/{seq}")
async def get_collected_data_by_seq(seq: int, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_data(db_session, logged_user, seq)
    return result

@app.get("/collected-data/user/{user_id}")
async def get_collected_dataUser_by_id(user_id: int, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_dataUser(db_session, logged_user, user_id)
    return result

@app.get("/collected-data/user/{id}/{type}")
async def get_collected_dataUser_by_id_type(id: int, type: int, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_dataUser(db_session, logged_user, id, type)
    return result

@app.post("/collected-data/")
async def post_collected_data(data: CollectedDataInput, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = post_data(db_session, data, logged_user)
    return result

@app.put("/collected-data/{seq}")
async def update_collected_data(seq: int, data: CollectedDataInput, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = put_data(db_session, data, seq, logged_user)
    return result

@app.delete("/collected-data/{seq}")
async def delete_collected_data(seq: int, db_session: Session = Depends(get_db), logged_user = Depends(get_logged_user)):
    result = delete_data(db_session, seq, logged_user)
    return result
