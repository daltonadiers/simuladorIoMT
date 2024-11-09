from pydantic import BaseModel
from pydantic import Field
from typing import List
import datetime

from collected_data import Collected_Data

class User(BaseModel):
    id: int
    name: str
    birth: datetime.date
    sex: str
    latitude: float
    longitude: float
    active: bool
    measure_types: List[int]
    measurements: List[Collected_Data] 