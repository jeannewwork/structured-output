from pydantic import BaseModel
from typing import Literal
from datetime import date

class Hotel(BaseModel):
    """
    Represents a hotel entity with its basic attributes.

    Attributes:
        id (int): Unique identifier for the hotel.
        name (str): The name of the hotel.
        address (str): The physical address of the hotel.
        tag (Literal["mountain", "city", "beach", "countryside"]): 
            The hotel's environment type.
    """
    id: int
    name: str
    address: str
    tag: Literal["mountain", "city", "beach", "countryside"]


class Room(BaseModel):
    """
    Represents a hotel room.

    Attributes:
        id (int): Unique identifier for the room.
        hotel_id (int): The ID of the hotel to which this room belongs.
        price (float): The price per night for the room.
        capacity (int): The maximum number of people the room can accommodate.
    """
    id: int
    hotel_id: int
    price: float
    capacity: int


class Option(BaseModel):
    """
    Represents an additional option or service.

    Attributes:
        id (int): Unique identifier for the option.
        name (str): The name of the option.
        tag (Literal["hotel", "room", "stay"]): Specifies whether the option applies to a hotel, a room, or a stay.
        price (float): The price of the option.
    """
    id: int
    name: str
    tag: Literal["hotel", "room", "stay"]
    price: float


class RoomOption(BaseModel):
    """
    Represents the association between a room and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        room_id (int): The ID of the room.
        option_id (int): The ID of the associated option.
    """
    id: int
    room_id: int
    option_id: int


class HotelOption(BaseModel):
    """
    Represents the association between a hotel and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        hotel_id (int): The ID of the hotel.
        option_id (int): The ID of the associated option.
    """
    id: int
    hotel_id: int
    option_id: int


class StayOption(BaseModel):
    """
    Represents the association between a stay and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        stay_id (int): The ID of the stay.
        option_id (int): The ID of the associated option.
    """
    id: int
    stay_id: int
    option_id: int


class Customer(BaseModel):
    """
    Represents a customer.

    Attributes:
        id (int): Unique identifier for the customer.
        name (str): The full name of the customer.
        mail (str): The email address of the customer.
    """
    id: int
    name: str
    mail: str


class Reservation(BaseModel):
    """
    Represents a room reservation by a customer.

    Attributes:
        id (int): Unique identifier for the reservation.
        customer_id (int): The ID of the customer making the reservation.
        room_id (int): The ID of the room being reserved.
        start_date (date): The check-in date of the reservation.
        end_date (date): The check-out date of the reservation.
    """
    id: int
    customer_id: int
    room_id: int
    start_date: date
    end_date: date