from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
from typing import Optional
from models import *
from security import *
from config import *
import requests
import logging

LOG = logging.getLogger(__name__)

def get_login(db_session: Session, email: str, password: str):
    try:
        user = db_session.query(User).filter(User.email == email).first()
        print(verify_password(password, user.password))
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=404, detail="Usuario não encontrado ou senha incorreta!")
        token = create_token(data_payload={'sub': user.email})
        return {'access_token': token, 'token_type': 'bearer'} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_user(db:Session, logged_user: User, seq: Optional[int] = None):
    try:
        admin = False
        if logged_user.email == 'admin@admin':
            admin = True
        
        if admin:
            if seq:
                results = db.query(User).filter(User.seq == seq).first()
            else: 
                results = db.query(User).all()
        else:
            results = db.query(User).filter(User.seq == logged_user.seq).first()
        
        if results:
            return results

        raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def post_user(db: Session, data: UserParameters):
    try:
        existing_user = db.query(User).filter(User.email == data.email).first()

        if existing_user:
            raise HTTPException(status_code=409, detail="E-mail já cadastrado")
        
        endereco = f"{data.street}, {data.house_number} - {data.city}, {data.state}"

        headers = {
            "User-Agent": "CadastrarUsuarios/1.0 (henriquepoerschke@gmail.com)"
        }
        
        response = requests.get(
            "https://nominatim.openstreetmap.org/search", 
            params={"q": endereco, "format": "json"}, 
            headers=headers
        )
        
        if response.ok and response.json():
            coordenadas = response.json()[0]

            hashed_pwd = get_password_hash(data.password)

            novo_usuario = User(
                name=data.name,
                email=data.email,
                password=hashed_pwd,
                birth=data.birth,
                sex=data.sex,
                latitude=float(coordenadas["lat"]),
                longitude=float(coordenadas["lon"]),
                active=True
            )

            db.add(novo_usuario)
            db.commit()
            db.refresh(novo_usuario)

            for t in data.types:
                novo_tipo = Types(userid=novo_usuario.seq,type=t)
                db.add(novo_tipo)

            db.commit()

            return {"message": "Usuário cadastrado com sucesso!", "user_seq": novo_usuario.seq}
        else:
            raise HTTPException(status_code=422, detail="Não foi possível obter coordenadas geográficas.")

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def put_user(db: Session, logged_user: User, data: UserParameters, seq: int):
    try:
        user = db.query(User).filter(User.seq == seq).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        if not (logged_user.email == "admin@admin" or seq == logged_user.seq):
            raise HTTPException(status_code=403, detail="Usuário sem permissão!")
        
        endereco = f"{data.street}, {data.house_number} - {data.city}, {data.state}"

        headers = {
            "User-Agent": "CadastrarUsuarios/1.0 (henriquepoerschke@gmail.com)"
        }
        
        response = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": endereco, "format": "json"},
            headers=headers
        )

        if response.ok and response.json():
            coordenadas = response.json()[0]

            user.name = data.name
            user.email = data.email
            user.password = pwd_context.hash(data.password)
            user.birth = data.birth
            user.sex = data.sex
            user.active = True
            user.latitude = coordenadas["lat"]
            user.longitude = coordenadas["lon"]
            db.commit()
            db.refresh(user)

        else:
            raise HTTPException(status_code=422, detail="Não foi possível obter coordenadas geográficas.")

        return {"message": "Usuário atualizado com sucesso", "seq": user.seq}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_user(db: Session, logged_user: User, seq: int):
    try:
        user = db.query(User).filter(User.seq == seq).first()

        if not (logged_user.email == "admin@admin" or seq == logged_user.seq):
            raise HTTPException(status_code=403, detail="Usuário sem permissão!")

        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        db.delete(user)
        db.commit()

        return {"message": "Usuário excluído com sucesso", "seq": seq}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))    

def get_types_by_user(db: Session, logged_user: User, seq: int):
    try:
        if not (logged_user.email == "admin@admin" or seq == logged_user.seq):
            raise HTTPException(status_code=403, detail="Usuário sem permissão!")

        results = db.query(Types).filter(Types.userid == seq).all()
                
        if results:
            return results

        raise HTTPException(status_code=404, detail="Dados não encontrados!")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_types_by_user(db: Session, logged_user: User, seq_user: int, types: int):
    try:
        if not (logged_user.email == "admin@admin" or seq_user == logged_user.seq):
            raise HTTPException(status_code=403, detail="Usuário sem permissão!") 
    
        type_to_delete = db.query(Types).filter(Types.type == types, Types.userid == seq_user).first()
        
        if not type_to_delete:
            raise HTTPException(status_code=404, detail="Type não encontrado") 
    
        db.delete(type_to_delete)
        db.commit()
    
        return {"message": "Type excluído com sucesso", "user_seq": seq_user, "type_deleted": types}
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
   
def post_type(db: Session, logged_user: User, seq_user: int, data: TypeInput):
    try:
    
        if not (logged_user.email == "admin@admin" or seq_user == logged_user.seq):
            raise HTTPException(status_code=403, detail="Usuário sem permissão!") 

        existing_type = db.query(Types).filter(Types.userid == seq_user, Types.type == data.type).first()
        if existing_type:
            raise HTTPException(status_code=409, detail="Type já existente para esse Usuário") 
    
        if data.type > 3 or data.type < 1:
            raise HTTPException(status_code=400, detail="Type inexistente!") 
    
        new_type = Types(
            type=data.type,
            userid=seq_user
        )
        
        db.add(new_type)
        db.commit()
        db.refresh(new_type)
        
        return {"message": "Type criado com sucesso!", "user_seq": seq_user}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e)) 
