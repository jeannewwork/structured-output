from pydantic import BaseModel, Field, root_validator
from typing import Literal
from datetime import date

class Hotel(BaseModel):
    """
    Represents a hotel entity with essential attributes.
    """
    id: int = Field(description="Unique identifier for the hotel", example=1)
    name: str = Field(description="Hotel name")
    address: str = Field(description="Full address of the hotel")
    tag: Literal["mountain", "city", "beach", "countryside"] = Field(
        description="Type of environment where the hotel is located",
    )

class Room(BaseModel):
    """
    Represents a hotel room.

    Attributes:
        id (int): Unique identifier for the room.
        hotel_id (int): The ID of the hotel this room belongs to.
        price (float): The price per night in euros. Must be greater than 0.
        capacity (int): The maximum number of people this room can accommodate. Must be at least 1.
    """
    id: int = Field(description="Unique identifier for the room", example=101)
    hotel_id: int = Field(description="ID of the hotel this room belongs to", example=1)
    price: float = Field(description="Price per night in euros", example=120.5)
    capacity: int = Field(description="Maximum number of guests", example=2)

    @root_validator(pre=True)
    def check_capacity(cls, values):
        """
        Ensures that capacity is at least 1.
        """
        if values.get("capacity", 0) < 1:
            raise ValueError("Capacity must be at least 1.")
        return values

class Option(BaseModel):
    """
    Represents an additional option or service available in a hotel.

    Attributes:
        id (int): Unique identifier for the option.
        name (str): The name of the option. Limited to 50 characters.
        tag (Literal): Indicates whether the option applies to a hotel, a room, or a stay.
        price (float): The price of the option in euros. Cannot be negative.
    """
    id: int = Field(description="Unique identifier for the option", example=10)
    name: str = Field(description="Name of the option", example="Breakfast Included", max_length=50)
    tag: Literal["hotel", "room", "stay"] = Field(
        description="Indicates whether the option applies to a hotel, a room, or a stay",
        example="room"
    )
    price: float = Field(description="Price of the option in euros", example=15.0, ge=0)

class RoomOption(BaseModel):
    """
    Represents the association between a room and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        room_id (int): The ID of the room this option is associated with.
        option_id (int): The ID of the associated option.
    """
    id: int = Field(description="Unique identifier for the room-option relation", example=201)
    room_id: int = Field(description="ID of the room linked to this option", example=101)
    option_id: int = Field(description="ID of the associated option", example=10)

class HotelOption(BaseModel):
    """
    Represents the association between a hotel and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        hotel_id (int): The ID of the hotel this option is associated with.
        option_id (int): The ID of the associated option.
    """
    id: int = Field(description="Unique identifier for the hotel-option relation", example=301)
    hotel_id: int = Field(description="ID of the hotel linked to this option", example=1)
    option_id: int = Field(description="ID of the associated option", example=10)

class StayOption(BaseModel):
    """
    Represents the association between a stay and an option.

    Attributes:
        id (int): Unique identifier for the relation.
        stay_id (int): The ID of the stay this option is associated with.
        option_id (int): The ID of the associated option.
    """
    id: int = Field(description="Unique identifier for the stay-option relation", example=401)
    stay_id: int = Field(description="ID of the stay linked to this option", example=5)
    option_id: int = Field(description="ID of the associated option", example=10)

class Customer(BaseModel):
    """
    Represents a customer making a reservation.

    Attributes:
        id (int): Unique identifier for the customer.
        name (str): Full name of the customer. Limited to 100 characters.
        mail (EmailStr): Valid email address of the customer.
    """
    id: int = Field(description="Unique identifier for the customer", example=1)
    name: str = Field(description="Full name of the customer", example="John Doe", max_length=100)
    mail: str = Field(description="Valid email address of the customer", example="johndoe@email.com")

class Reservation(BaseModel):
    """
    Represents a room reservation by a customer.

    Attributes:
        id (int): Unique identifier for the reservation.
        customer_id (int): The ID of the customer making the reservation.
        room_id (int): The ID of the reserved room.
        start_date (date): The check-in date of the reservation.
        end_date (date): The check-out date of the reservation.
    """
    id: int = Field(description="Unique identifier for the reservation", example=501)
    customer_id: int = Field(description="ID of the customer making the reservation", example=1)
    room_id: int = Field(description="ID of the reserved room", example=101)
    start_date: str = Field(description="Check-in date of the reservation", example="2025-06-01")
    end_date: str = Field(description="Check-out date of the reservation", example="2025-06-10")