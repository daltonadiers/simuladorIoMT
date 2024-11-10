from fastapi import FastAPI
from contextlib import asynccontextmanager
import psycopg2
from collected_data_actions import *

from collected_data import Collected_Data_Input

cursor: psycopg2.extensions.cursor

@asynccontextmanager
async def lifespan(app: FastAPI):
    global cursor
    cursor = connect_db()
    yield
    close_db()

app = FastAPI(lifespan=lifespan)

@app.get("/collected-data/")
async def get_collected_data():
    result = get_data(cursor)
    return result

@app.get("/collected-data/{seq}")
async def get_collected_data_by_seq(seq: int):
    result = get_data(cursor, seq)
    return result

@app.post("/collected-data/")
async def post_collected_data(data: Collected_Data_Input):
    result = post_data(cursor, data)
    return result

@app.put("/collected-data/{seq}")
async def update_collected_data(seq: int, data: Collected_Data_Input):
    result = put_data(cursor, data, seq)
    return result

@app.delete("/collected-data/{seq}")
async def delete_collected_data(seq: int):
    result = delete_data(cursor, seq)
    return result
