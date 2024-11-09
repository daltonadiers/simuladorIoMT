from pydantic import BaseModel
from pydantic import Field
import datetime

class Collected_Data_Input(BaseModel):
    userid: int
    type: int
    value1: float
    value2: float

class Collected_Data(BaseModel):
    seq: int
    userid: int
    colected_date: datetime.datetime
    sensor_type: int
    value1: float
    value2: float
    inhouse: bool