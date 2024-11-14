from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import User, UserInput
from typing import Optional
from datetime import datetime
import logging

LOG = logging.getLogger(__name__)

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

def post_user(db: Session, data:UserInput):
    try:
        new_user = User (
            name = data.name,
            email = data.email,
            password = data.password,
            birth = data.birth,
            sex = data.sex,
            latitude = data.latitude,
            longitude = data.longitude,
            active = data.active
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message" : "Usuário criado com sucesso!", "seq": new_user}

    except Exception as e:
        db.rollback()
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
    