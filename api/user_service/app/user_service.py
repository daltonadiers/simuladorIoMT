from models import *
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
from user_actions import *
from typing import List
from security import *
from database import *
import logging
from config import ORIGINS


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/token', response_model=Token)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db_session: Session = Depends(get_db)):
     token = get_login(db_session, form_data.username, form_data.password)
     return token

@app.get("/users/")
async def get_users(db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_user(db_session, logged_user)
    return result
    
@app.get("/users/{seq}")
async def get_users_by_id(seq: int, db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    result = get_user(db_session, logged_user, seq)
    return result

@app.post("/users/")
async def post_users(data: UserParameters, db_session: Session=Depends(get_db)):
    result = post_user(db_session, data)
    return result

@app.put("/users/{seq}")
async def put_users(seq:int, data: UserParameters, db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    result = put_user(db_session, logged_user, data, seq)
    return result

@app.delete("/users/{seq}")
async def delete_users(seq:int , db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    result = delete_user(db_session, logged_user, seq)
    return result

@app.get("/users/{seq}/types/", response_model=List[TypeOutput])
async def get_user_types(seq: int, db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    types = get_types_by_user(db_session, logged_user,seq)
    return types

@app.delete("/users/{seq_user}/types/{type}")
async def delete_user_types(seq_user: int, type: int, db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    types = delete_types_by_user(db_session, logged_user, seq_user, type)
    return types

@app.post("/users/{seq_user}/types/{type}")
async def post_user_types(seq_user: int, data: TypeInput, db_session: Session=Depends(get_db), logged_user = Depends(get_logged_user)):
    types = post_type(db_session, logged_user, seq_user, data)
    return types
