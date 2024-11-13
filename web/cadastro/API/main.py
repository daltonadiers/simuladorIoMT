import os
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, String, Integer, DateTime, Boolean, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Usuario(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    birth = Column(DateTime, nullable=False)
    sex = Column(String, nullable=False)
    latitude = Column(Numeric, nullable=False)
    longitude = Column(Numeric, nullable=False)
    active = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

class Parameters(BaseModel):
    name: str
    birth: datetime
    sex: str
    cep: str
    estado: str
    cidade: str
    bairro: str
    rua: str
    numero: str

@app.post("/api/cadastro")
def cadastrar_usuario(usuario: Parameters, db: Session = Depends(get_db)):
    endereco = f"{usuario.rua}, {usuario.numero} - {usuario.cidade}, {usuario.estado}"

    headers = {
        "User-Agent": "CadastrarUsuarios/1.0 (henriquepoerschke@gmail.com)"
    }
    
    response = requests.get(f"https://nominatim.openstreetmap.org/search", params={"q": endereco, "format": "json"}, headers=headers)
    
    if response.ok and response.json():
        coordenadas = response.json()[0]

        novo_usuario = Usuario(
            name=usuario.name,
            birth=usuario.birth,
            sex=usuario.sex,
            latitude=float(coordenadas['lat']),
            longitude=float(coordenadas['lon']),
            active=False
        )

        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)

        return {"message": "Usuário cadastrado com sucesso!", "usuario_id": novo_usuario.id}
    else:
        raise HTTPException(status_code=400, detail="Não foi possível obter coordenadas geográficas.")
