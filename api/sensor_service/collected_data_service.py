from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

from collected_data import Collected_Data, Collected_Data_Input

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_connection = psycopg2.connect(
        DATABASE_URL, cursor_factory=RealDictCursor
    )
    print("Conectado ao banco de dados")
    yield
    app.state.db_connection.close()
    print("Desconectado do banco de dados")

app = FastAPI(lifespan=lifespan)

@app.get("/collected-data/")
async def get_collected_data():
    with app.state.db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM collected_data')
        result = cursor.fetchall()
    return {"data": result}

@app.get("/collected-data/{seq}")
async def get_collected_data_by_seq(seq: int):
    with app.state.db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM collected_data WHERE seq = %s', (seq,))
        result = cursor.fetchone()
    if result is None:
        raise HTTPException(status_code=404, detail="Dados não encontrados")
    return {"data": result}

@app.post("/collected-data/")
async def post_collected_data(data: Collected_Data_Input):
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
        with app.state.db_connection.cursor() as cursor:
            cursor.execute(sql, values)
            new_seq = cursor.fetchone()['seq']
            app.state.db_connection.commit()
        return {"message": "Dados inseridos com sucesso", "seq": new_seq}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/collected-data/{seq}")
async def update_collected_data(seq: int, data: Collected_Data_Input):
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
        with app.state.db_connection.cursor() as cursor:
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Dados não encontrados")
            app.state.db_connection.commit()
        return {"message": "Dados atualizados com sucesso"}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/collected-data/{seq}")
async def delete_collected_data(seq: int):
    try:
        with app.state.db_connection.cursor() as cursor:
            cursor.execute('DELETE FROM collected_data WHERE seq = %s', (seq,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Dados não encontrados")
            app.state.db_connection.commit()
        return {"message": "Dados deletados com sucesso"}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
