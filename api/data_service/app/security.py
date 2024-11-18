from passlib.context import CryptContext
from jwt import encode, decode
from jwt.exceptions import PyJWTError
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES
from models import User

pwd_context = CryptContext(schemes=['bcrypt'])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)

def create_token(data_payload: dict):
    to_encode = data_payload.copy()
    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)

    to_encode.update({'exp': expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_logged_user(db_session: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get('sub')
        if not username:
            raise HTTPException(status_code=500, detail="Credenciais inválidas!")
        
        logged_user = db_session.query(User).filter(User.email == username).first()
        if not logged_user:
            raise HTTPException(status_code=500, detail="Usuário não existe!")

        return logged_user
    except PyJWTError as e:
        raise HTTPException(status_code=500, detail="Credenciais inválidas!")