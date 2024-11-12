from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import CollectedData, CollectedDataInput
from typing import Optional
from datetime import datetime
import logging

LOG = logging.getLogger(__name__)

def get_data(db: Session, seq: Optional[int] = None):
    try:
        if seq:
            results = db.query(CollectedData).filter(CollectedData.seq == seq).first()
        else: 
            results = db.query(CollectedData).all()

        if results:
            return results
        else:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def post_data(db: Session, data: CollectedDataInput):
    try:
        new_data = CollectedData(
            userid=data.userid,
            datetime=datetime.now(),
            type=data.type_,
            value1=data.value1,
            value2=data.value2,
            inhouse=False
        )

        db.add(new_data)
        db.commit()
        db.refresh(new_data)

        return {"message": "Dados inseridos com sucesso", "seq": new_data}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def put_data(db: Session, data: CollectedDataInput, seq: int):
    try:
        existing_data = db.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")

        existing_data.userid = data.userid
        existing_data.type = data.type_
        existing_data.value1 = data.value1
        existing_data.value2 = data.value2
        existing_data.inhouse = False

        db.commit()
        db.refresh(existing_data)

        return {"message": "Dados atualizados com sucesso", "seq": existing_data.seq}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_data(db: Session, seq: int):
    try:
        existing_data = db.query(CollectedData).filter(CollectedData.seq == seq).first()

        if not existing_data:
            raise HTTPException(status_code=404, detail="Dados não encontrados!")

        db.delete(existing_data)
        db.commit()

        return {"message": "Dados excluídos com sucesso", "seq": seq}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))