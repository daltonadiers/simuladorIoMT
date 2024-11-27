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
        return {'access_token': token, 'token_type': 'bearer'} 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_data(db_session: Session, logged_user: User, seq: Optional[int] = None):
    try:
        admin = False
        if logged_user.email == "admin@admin":
            admin = True
        if seq:
            if admin:
                results = db_session.query(CollectedData).filter(CollectedData.seq == seq).order_by(CollectedData.seq).all()
            else:
                results = db_session.query(CollectedData).filter(CollectedData.seq == seq, CollectedData.userid == logged_user.seq).order_by(CollectedData.seq).all()
        else:
            if admin:
                results = db_session.query(CollectedData).order_by(CollectedData.seq).all()
            else:
                results = db_session.query(CollectedData).filter(CollectedData.userid == logged_user.seq).order_by(CollectedData.seq).all()

        if results:
            return results_formater(results)
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados ou inexistentes para esse usuario!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_dataUser(db_session: Session, logged_user: User, user_id: int, type: Optional[int] = None):
    try:
        if (user_id != logged_user.seq) & (logged_user.email != "admin@admin"):
            raise HTTPException(status_code=404, detail="Usuario sem direitos para visualizar esse usuário!")

        if type:
            results = db_session.query(CollectedData).filter(CollectedData.userid == user_id, CollectedData.type == type).order_by(CollectedData.seq).all()
        else:
            results = db_session.query(CollectedData).filter(CollectedData.userid == user_id).order_by(CollectedData.seq).all()

        if results:
            return results_formater(results)
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
         
def post_data(db_session: Session, data: CollectedDataInput, logged_user: User):
    try:
        if logged_user.email == "admin@admin":
            new_data = CollectedData(
            userid=data.userid,
            datetime=datetime.now(),
            type=data.type_,
            value1=data.value1,
            value2=data.value2,
            inhouse=data.inhouse
        )
        elif ((data.userid) == 0 or (data.userid == logged_user.seq)):
            new_data = CollectedData(
                userid=logged_user.seq,
                datetime=datetime.now(),
                type=data.type_,
                value1=data.value1,
                value2=data.value2,
                inhouse=data.inhouse
            )
        else:
            raise HTTPException(status_code=500, detail="Usuario sem direitos para inserir esse dado!")

        db_session.add(new_data)
        db_session.commit()
        db_session.refresh(new_data)

        return {"message": "Dados inseridos com sucesso", "seq": new_data}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def put_data(db_session: Session, data: CollectedDataInput, seq: int, logged_user: User):
    try:
        existing_data = db_session.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")

        if logged_user.email == "admin@admin":
            existing_data.userid = data.userid
            existing_data.type = data.type_
            existing_data.value1 = data.value1
            existing_data.value2 = data.value2
            existing_data.inhouse = data.inhouse
        elif existing_data.userid != logged_user.seq:
            raise HTTPException(status_code=500, detail="Usuario sem direitos para atualizar esse dado!")
        elif ((data.userid == 0) or (data.userid == logged_user.seq)):
            existing_data.type = data.type_
            existing_data.value1 = data.value1
            existing_data.value2 = data.value2
            existing_data.inhouse = data.inhouse
        else:
            raise HTTPException(status_code=500, detail="Usuario sem direitos para atualizar esse dado!")

        db_session.commit()
        db_session.refresh(existing_data)

        return {"message": "Dados atualizados com sucesso", "seq": existing_data.seq}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_data(db_session: Session, seq: int, logged_user: User):
    try:
        existing_data = db_session.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")
        
        if (existing_data.userid != logged_user.seq) and (logged_user.email != "admin@admin"):
            raise HTTPException(status_code=500, detail="Usuario sem direitos para atualizar esse dado!")

        db_session.delete(existing_data)
        db_session.commit()

        return {"message": "Dados excluídos com sucesso", "seq": seq}
    except Exception as e:
        db_session.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def results_formater(results: list):
    return [{"seq": r.seq,"type": r.type, "userid": r.userid,"value1": r.value1,
                     "value2": r.value2, "datetime": r.datetime, "inhouse": r.inhouse} for r in results]