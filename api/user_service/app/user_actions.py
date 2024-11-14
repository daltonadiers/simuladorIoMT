from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import *
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

def post_user(db: Session, data: UserInput):
    try:
        new_user = User(
            name=data.name,
            email=data.email,
            password=data.password, 
            birth=data.birth,
            sex=SexType(data.sex), 
            latitude=data.latitude,
            longitude=data.longitude,
            active=data.active
        )

        new_types = []
        for idx, val in enumerate(data.types):
            if val == 1:
                new_type = Types(
                    type=idx + 1, 
                    user=new_user 
                )
                new_types.append(new_type)

        new_user.types = new_types

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Usuário criado com sucesso!", "seq": new_user.seq}

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
