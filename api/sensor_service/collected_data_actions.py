from fastapi import HTTPException
import psycopg2.extensions
import psycopg2
from psycopg2.extras import RealDictCursor
from collected_data import Collected_Data_Input
import os
from dotenv import load_dotenv
from typing import Optional
from datetime import datetime
import logging

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

db_connection: psycopg2.connect

LOG = logging.getLogger(__name__)

def connect_db() -> psycopg2.extensions.cursor:
    global db_connection
    try:
        db_connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
        LOG.info("Connected to DB!")
        return db_connection.cursor()
    except Exception as e:
        LOG.error(f"Error connecting to DB: {e}")


def close_db():
    global db_connection
    db_connection.close()

def get_data(cursor: psycopg2.extensions.cursor, seq: Optional[int] = None):
    query = 'SELECT * FROM collected_data c'
    if seq:
        query += ' WHERE c.seq = %s'
        cursor.execute(query, (seq,))
        result = cursor.fetchall()
    else:
        query += ' ORDER BY c.seq'
        cursor.execute(query)
        result = cursor.fetchall()
    
    if result:
        return {"data": result}
    else:
        raise HTTPException(status_code=404, detail="Dados não encontrados")

def post_data(cursor: psycopg2.extensions.cursor, data: Collected_Data_Input):
    sql = '''
        INSERT INTO collected_data (userid, "type", value1, value2, "datetime", inhouse)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING seq
    '''
    values = (
        data.userid,
        data.type_,
        data.value1,
        data.value2,
        datetime.now(),
        False
    )
    try:
        cursor.execute(sql, values)
        new_seq = cursor.fetchone()['seq']
        db_connection.commit()
        return {"message": "Dados inseridos com sucesso", "seq": new_seq}
    except Exception as e:
        db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def put_data(cursor: psycopg2.extensions.cursor, data: Collected_Data_Input, seq: int):
    sql = '''
        UPDATE collected_data
        SET userid = %s, "type" = %s, value1 = %s, value2 = %s, "datetime" = %s, inhouse = %s
        WHERE seq = %s
    '''
    values = (
        data.userid,
        data.type_,
        data.value1,
        data.value2,
        datetime.now(),
        False,
        seq
    )
    try:
        cursor.execute(sql, values)
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dados não encontrados")
        db_connection.commit()
        result = get_data(cursor, seq)
        return {"message": "Dados atualizados com sucesso", 
                "updated": result}
    except Exception as e:
        db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def delete_data(cursor: psycopg2.extensions.cursor, seq: int):
    try:
        result = get_data(cursor, seq)
        cursor.execute('DELETE FROM collected_data WHERE seq = %s', (seq,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Dados não encontrados")
        db_connection.commit()
        return {"message": "Dados deletados com sucesso", "deleted": result}
    except Exception as e:
        db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))