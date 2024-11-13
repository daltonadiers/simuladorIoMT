from pydantic import BaseModel, Field
import datetime

class Collected_Data_Input(BaseModel):
    userid: int
    type_: int = Field(alias='type') 
    value1: float
    value2: float

class Collected_Data(BaseModel):
    seq: int
    userid: int
    datetime_: datetime.datetime = Field(alias='datetime') 
    type_: int = Field(alias='type')
    value1: float
    value2: float
    inhouse: bool
