from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime

from collected_data import Collected_Data
from collected_data import Collected_Data_Input

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_connection = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    print("Conectado ao banco de dados")
    yield
    app.state.db_connection.close()
    print("Desconectado do banco de dados")

app = FastAPI(lifespan=lifespan)

@app.get("/collected-data/")
async def get_collected_data():
    with app.state.db_connection.cursor() as cursor:
        cursor.execute("SELECT * FROM collected_data")
        result = cursor.fetchall()
    return {"data": result}

@app.post("/collectd-data/")
async def post_collected_data(data: Collected_Data_Input):
    sql = """
            INSERT INTO collected_data (userid, type, value1, value2, datetime, inhouse)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    values = (data.userid, data.type, data.value1, data.value2, datetime.now(), False)
    try:
        with app.state.db_connection.cursor() as cursor:
            cursor.execute(sql, values)
            app.state.db_connection.commit()
        return {"message": "Dados inseridos com sucesso"}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
