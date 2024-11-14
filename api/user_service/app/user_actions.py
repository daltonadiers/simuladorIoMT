from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from models import *
import requests
import logging

LOG = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=['bcrypt'])

def get_user(db:Session, seq: Optional[int] = None):
    try:
        if seq:
            results = db.query(User).filter(User.seq == seq).first()
        else: 
            results = db.query(User).all()
        
        if results:
            return results

        raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def post_user(db: Session, data: UserParameters):
    try:
        endereco = f"{data.street}, {data.house_number} - {data.city}, {data.state}"

        headers = {
            "User-Agent": "CadastrarUsuarios/1.0 (henriquepoerschke@gmail.com)"
        }
        
        response = requests.get(f"https://nominatim.openstreetmap.org/search", params={"q": endereco, "format": "json"}, headers=headers)
        
        if response.ok and response.json():
            coordenadas = response.json()[0]

            hashed_pwd = pwd_context.hash(data.password)

            novo_usuario = User(
                name=data.name,
                email=data.email,
                password=hashed_pwd,
                birth=data.birth,
                sex=data.sex,
                latitude=float(coordenadas['lat']),
                longitude=float(coordenadas['lon']),
                active=True
            )

            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)

            return {"message": "Usuário cadastrado com sucesso!", "usuario_id": novo_usuario.id}
        else:
            raise HTTPException(status_code=400, detail="Não foi possível obter coordenadas geográficas.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def login(db:Session, data: LoginParameters):
    try:
        user: User = db.query(User).filter(User.email == data.email)

        if not user:
            raise HTTPException(status_code=401, detail="Usuário ou Senha incorretos")

        flag_pwd_correct = pwd_context.verify(data.password, user.password)

        if flag_pwd_correct:
            return {"message": "Login realizado com sucesso"}

        raise HTTPException(status_code=401, detail="Usuário ou Senha incorretos")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def put_user(db:Session, data:UserInput, seq:int):
    try:
        user = db.query(User).filter(User.seq==seq).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        user.name = data.name
        user.email = data.email
        user.password = data.password
        user.birth = data.birth
        user.sex = data.sex
        user.latitude = data.latitude
        user.longitude = data.longitude
        user.active = data.active
        
        db.commit()
        db.refresh(user)

        return {"message": "Usuario atualizado com sucesso", "seq": user.seq}


    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
def delete_user(db:Session, seq:int):
    try:
        user = db.query(User).filter(User.seq==seq).first()
        
        if not user:
            raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    
        db.delete(user)
        db.commit()
    
        return {"message": "Usuario excluído com sucesso", "seq": seq}

    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, datail=str(e))
    
def get_types_by_user(db: Session, seq: int):
    try:
        results = db.query(Types).filter(Types.userid == seq).all()
        
        if results:
            return results

        raise HTTPException(status_code=404, detail="Dados não encontrados!")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_types_by_user(db: Session, seq_user: int,  types= int):
    try:
        types = db.query(Types).filter(Types.type == types, Types.userid == seq_user).first()
        
        
        if not types:
            raise HTTPException(status_code=404, detail="Type não encontrado")
    
        db.delete(types)
        db.commit()
    
        return {"message": "Type excluído com sucesso", "user_seq": seq_user, "Type Deleted": types}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, datail=str(e))
    
    
def post_type(db: Session, seq_user: int, data: TypeInput):
    try:
            
        new_type = db.query(Types).filter(Types.userid == seq_user, Types.type == data.type).first()
        
        if new_type:
            raise HTTPException(status_code=401, detail="Type já existente para esse Usuário")


        if data.type > 3 or data.type < 1:
            raise HTTPException(status_code=401, detail="Type inexistente!")

        new_type = Types(
                type = data.type,
                userid = seq_user
            )
        

        db.add(new_type)
        db.commit()
        db.refresh(new_type)
        
        return {"message": "Type criado com sucesso!", "user_seq": seq_user}

        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))    
