import os
from openai import OpenAI
from dotenv import load_dotenv
import json
import random
from pydantic import BaseModel
from typing import Type, List, get_args, Literal

from structured_output.class_database import Hotel, Room, Option, RoomOption, HotelOption, StayOption, Customer, Reservation
from structured_output.utils import append_to_json, parse_openai_response, get_system_prompt_for_class, get_associated_tables, load_existing_data, get_user_prompt_system, get_data

load_dotenv()

client = OpenAI(
    base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = "gpt-4o-mini"

def generate_partial_data(model: Type[BaseModel], n: int, existing_data: List[dict] = None) -> List[BaseModel]:
    generated_data = []

    if existing_data:
        last_id = max((item["id"] for item in existing_data), default=0)
    else:
        last_id = 0

    for i in range(1, n + 1):
        obj_data = {}

        for field_name, field in model.__annotations__.items():
            if field_name == "id":
                obj_data[field_name] = last_id + i  
            elif hasattr(field, "__origin__") and field.__origin__ is Literal:
                obj_data[field_name] = random.choice(get_args(field))  
            else:
                obj_data[field_name] = "à compléter"
        generated_data.append(model(**obj_data))

    return generated_data


def generate_response(class_name: str, response_format, data_path: str, obj_id: int):

    system_prompt = get_system_prompt_for_class(class_name)

    obj_to_complete = get_data(data_path, obj_id)

    user_prompt = (
    "Complete the following data while strictly preserving the existing values. "
    "Ensure that all present fields remain unchanged. "
    "Generate only the missing values in a coherent and contextually appropriate manner based on the provided information.\n\n"
    f"{json.dumps(obj_to_complete, indent=4, ensure_ascii=False)}"
)

    response = client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=response_format,
    )

    generated_data = json.loads(response.choices[0].message.content.strip())

    if generated_data["id"] != obj_id:
        generated_data["id"] = obj_id
    

    return response_format(**generated_data)


if __name__ == "__main__":
    class_name = "Hotel"
    data_path = "/Users/datacraft/structured-output/data/hotel.json"

    print("🔄 Génération de la base partielle...")
    partial_hotels = generate_partial_data(Hotel, n=5) 

    with open(data_path, "w", encoding="utf-8") as file:
        json.dump([hotel.model_dump() for hotel in partial_hotels], file, indent=4, ensure_ascii=False)
    
    print(f"✅ Base partielle enregistrée dans {data_path}")

    completed_hotels = []
    
    print("🔄 Complétion des hôtels avec l'IA...")
    for hotel in partial_hotels:
        completed_hotel = generate_response(class_name, Hotel, data_path, hotel.id)
        completed_hotels.append(completed_hotel)

    with open(data_path, "w", encoding="utf-8") as file:
        json.dump([hotel.dict() for hotel in completed_hotels], file, indent=4, ensure_ascii=False)

    print(f"✅ Base complétée enregistrée dans {data_path}")
