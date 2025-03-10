import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import random
from datetime import date
from pydantic import BaseModel
from typing import Type, List, Literal, Any, Dict, get_args


from structured_output.class_database import Hotel, Option, Reservation, Room, Customer 
from structured_output.utils import get_system_prompt_for_class, get_data, generate_user_prompt, save_data

load_dotenv()

client = OpenAI(
    base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = "gpt-4o"

def generate_partial_data(model: Type[BaseModel], n: int, existing_data: List[Dict[str, Any]] = None) -> List[BaseModel]:
    """
    Generates a list of partially completed objects based on the given Pydantic model.

    - The `id` field is incremented sequentially.
    - Literal fields are randomly assigned values.
    - Other fields are initialized with "to be completed".

    Args:
        model (Type[BaseModel]): The Pydantic model class.
        n (int): Number of objects to generate.
        existing_data (List[Dict[str, Any]], optional): Existing database to avoid duplicate IDs.

    Returns:
        List[BaseModel]: List of partially completed model instances.
    """
    generated_data = []

    last_id = max((item["id"] for item in existing_data), default=0) if existing_data else 0

    for i in range(1, n + 1):
        obj_data: Dict[str, Any] = {}

        for field_name, field_type in model.__annotations__.items():
            if field_name == "id":
                obj_data[field_name] = last_id + i  # Incremental ID
            elif hasattr(field_type, "__origin__") and field_type.__origin__ is Literal:
                obj_data[field_name] = random.choice(get_args(field_type))  # Random Literal selection
            elif field_type == float:  
                obj_data[field_name] = 0.0  
            elif field_type == int:
                obj_data[field_name] = 1 
            elif field_type == str:
                obj_data[field_name] = "2025-06-01"
            else:
                obj_data[field_name] = "null"

        generated_data.append(model(**obj_data))

    return generated_data



def generate_response(class_name: str, response_format: Type[BaseModel], data_path: str, obj_id: int) -> BaseModel:
    """
    Generates missing values for a given object while preserving existing fields.

    Args:
        class_name (str): The class name (e.g., "Hotel").
        response_format (Type[BaseModel]): The Pydantic model for validation.
        data_path (str): Path to the database file.
        obj_id (int): ID of the object to complete.

    Returns:
        BaseModel: The completed and validated object.
    """
    system_prompt = get_system_prompt_for_class(class_name)
    obj_to_complete = get_data(data_path, obj_id)
    user_prompt = generate_user_prompt(obj_to_complete)

    response = client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=response_format,
        temperature=1.5,
    )

    generated_data = json.loads(response.choices[0].message.content.strip())

    if generated_data["id"] != obj_id:
        generated_data["id"] = obj_id 

    return response_format(**generated_data)


if __name__ == "__main__":
    class_name = "Room"
    data_path = "/Users/datacraft/structured-output/data/room.json"

    partial_hotels = generate_partial_data(Room, n=10)

    save_data(partial_hotels, data_path)

    completed_hotels = []

    for hotel in partial_hotels:
        completed_hotel = generate_response(class_name, Room, data_path, hotel.id)
        completed_hotels.append(completed_hotel)

    save_data(completed_hotels, data_path)

