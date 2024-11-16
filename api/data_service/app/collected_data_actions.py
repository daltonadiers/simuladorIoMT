from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import CollectedData, CollectedDataInput, User
from typing import Optional
from datetime import datetime
import logging
from security import verify_password, create_token

LOG = logging.getLogger(__name__)

def get_login(db_session: Session, email: str, password: str):
    try:
        user = db_session.query(User).filter(User.email == email).first()
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=404, detail="Usuario não encontrado ou senha incorreta!")
        token = create_token(data_payload={'sub': user.email})
        return {'acess_token': token, 'token_type': 'Bearer'}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_data(db_session: Session, seq: Optional[int] = None):
    try:
        if seq:
            results = db_session.query(CollectedData).filter(CollectedData.seq == seq).order_by(CollectedData.seq).all()
        else: 
            results = db_session.query(CollectedData).order_by(CollectedData.seq).all()

        if results:
            return results_formater(results)
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_dataUser(db_session: Session, id: int, type: Optional[int] = None):
    try:
        if type:
            results = db_session.query(CollectedData).filter(CollectedData.userid == id, CollectedData.type == type).order_by(CollectedData.seq).all()
        else:
            results = db_session.query(CollectedData).filter(CollectedData.userid == id).order_by(CollectedData.seq).all()

        if results:
            return results_formater(results)
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
         

def post_data(db_session: Session, data: CollectedDataInput):
    try:
        new_data = CollectedData(
            userid=data.userid,
            datetime=datetime.now(),
            type=data.type_,
            value1=data.value1,
            value2=data.value2,
            inhouse=data.inhouse
        )

        db_session.add(new_data)
        db_session.commit()
        db_session.refresh(new_data)

        return {"message": "Dados inseridos com sucesso", "seq": new_data}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def put_data(db_session: Session, data: CollectedDataInput, seq: int):
    try:
        existing_data = db_session.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")

        existing_data.userid = data.userid
        existing_data.type = data.type_
        existing_data.value1 = data.value1
        existing_data.value2 = data.value2
        existing_data.inhouse = data.inhouse

        db_session.commit()
        db_session.refresh(existing_data)

        return {"message": "Dados atualizados com sucesso", "seq": existing_data.seq}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_data(db_session: Session, seq: int):
    try:
        existing_data = db_session.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")

        db_session.delete(existing_data)
        db_session.commit()

        return {"message": "Dados excluídos com sucesso", "seq": seq}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def results_formater(results: list):
    return [{"seq": r.seq,"type": r.type, "userid": r.userid,"value1": r.value1,
                     "value2": r.value2, "datetime": r.datetime, "inhouse": r.inhouse} for r in results]