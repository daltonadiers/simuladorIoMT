from pydantic import BaseModel, Field
from sqlalchemy import (
    Column, Integer, String, Date, Float, Boolean, ForeignKey, TIMESTAMP
)
from typing import List, Optional

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Enum as PgEnum
import enum
import datetime

Base = declarative_base()

class SexType(enum.Enum):
    M = 'M'
    F = 'F'

class User(Base):
    __tablename__ = 'users'
    
    seq = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    birth = Column(Date, nullable=False)
    sex = Column(PgEnum(SexType), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    
    types = relationship("Types", back_populates="user", cascade="all, delete-orphan")
    collected_data = relationship("CollectedData", back_populates="user", cascade="all, delete-orphan")

class CollectedData(Base):
    __tablename__ = 'collected_data'
    
    seq = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.seq', ondelete='CASCADE'), nullable=False)
    datetime = Column(TIMESTAMP, nullable=False)
    type = Column(Integer)
    value1 = Column(Float)
    value2 = Column(Float)
    inhouse = Column(Boolean)
    
    user = relationship("User", back_populates="collected_data")

class CollectedDataInput(BaseModel):
    userid: int
    type_: int = Field(alias='type') 
    value1: float
    value2: float
    inhouse: bool

class UserInput(BaseModel):
    name: str
    email: str
    password:str
    birth: datetime.date
    sex: str
    latitude: float
    longitude: float
    active: bool
    types:List[int]
    
class Types(Base):
    __tablename__ = 'types'
    seq = Column(Integer, primary_key=True, index=True)
    userid = Column(Integer, ForeignKey('users.seq', ondelete='CASCADE'), nullable=False)
    type = Column(Integer)

    user = relationship("User", back_populates="types")


class TypeInput(BaseModel):
    type: int


class TypeOutput(BaseModel):
    seq: int
    userid: int
    type: int
