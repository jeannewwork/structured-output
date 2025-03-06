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


class Option(BaseModel):
    id: int 
    name: str 
    tag: Literal["hotel", "room", "stay"]
    price: float


class RoomOption(BaseModel):
    id: int
    room_id: int
    option_id: int 


class HotelOption(BaseModel):
    id: int
    hotel_id: int
    option_id: int 


class StayOption(BaseModel):
    id: int
    stay_id: int
    option_id: int 
