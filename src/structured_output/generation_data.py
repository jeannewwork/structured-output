from pydantic import BaseModel
from typing import Literal


class Hotel(BaseModel):
    id: int 
    name: str
    address: str
    tag: Literal["montagne", "plage", "ville", "campagne"]

class Room(BaseModel):
    id: int 
    hotel_id: int 
    price: float
    capacity: int
