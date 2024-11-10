# user_service.py
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List

from user import User, UserInput
from collected_data import Collected_Data

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

@app.get("/users/")
async def get_users():
    with app.state.db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users')
        users = cursor.fetchall()
        for user in users:
            user_id = user['id']
            # Fetch measurements for the user
            cursor.execute('SELECT * FROM collected_data WHERE userid = %s', (user_id,))
            measurements = cursor.fetchall()
            user['measurements'] = measurements
    return {"data": users}

@app.get("/users/{id}")
async def get_user_by_id(id: int):
    with app.state.db_connection.cursor() as cursor:
        cursor.execute('SELECT * FROM users WHERE id = %s', (id,))
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        # Fetch measurements for the user
        cursor.execute('SELECT * FROM collected_data WHERE userid = %s', (id,))
        measurements = cursor.fetchall()
        user['measurements'] = measurements
    return {"data": user}

@app.post("/users/")
async def create_user(user_input: UserInput):
    sql = '''
        INSERT INTO users (name, birth, sex, latitude, longitude, active)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING id
    '''
    values = (
        user_input.name,
        user_input.birth,
        user_input.sex,
        user_input.latitude,
        user_input.longitude,
        user_input.active
    )
    try:
        with app.state.db_connection.cursor() as cursor:
            cursor.execute(sql, values)
            user_id = cursor.fetchone()['id']
            app.state.db_connection.commit()
        return {"message": "Usuário criado com sucesso", "id": user_id}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/users/{id}")
async def update_user(id: int, user_input: UserInput):
    sql = '''
        UPDATE users
        SET name = %s, birth = %s, sex = %s, latitude = %s, longitude = %s, active = %s
        WHERE id = %s
    '''
    values = (
        user_input.name,
        user_input.birth,
        user_input.sex,
        user_input.latitude,
        user_input.longitude,
        user_input.active,
        id
    )
    try:
        with app.state.db_connection.cursor() as cursor:
            cursor.execute(sql, values)
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            app.state.db_connection.commit()
        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/users/{id}")
async def delete_user(id: int):
    try:
        with app.state.db_connection.cursor() as cursor:
            cursor.execute('DELETE FROM users WHERE id = %s', (id,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Usuário não encontrado")
            app.state.db_connection.commit()
        return {"message": "Usuário deletado com sucesso"}
    except Exception as e:
        app.state.db_connection.rollback()
        raise HTTPException(status_code=500, detail=str(e))
