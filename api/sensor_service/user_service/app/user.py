# user.py
from pydantic import BaseModel
from typing import List, Optional
import datetime

from collected_data import Collected_Data

class UserInput(BaseModel):
    name: str
    birth: datetime.date
    sex: str
    latitude: float
    longitude: float
    active: bool
    measure_types: List[int]

class User(BaseModel):
    id: int
    name: str
    birth: datetime.date
    sex: str
    latitude: float
    longitude: float
    active: bool
    measure_types: List[int]
    measurements: Optional[List[Collected_Data]] = []
