import os
from openai import OpenAI
from dotenv import load_dotenv

from structured_output.class_database import Hotel, Room, Option, RoomOption, HotelOption, StayOption, Customer, Reservation
from structured_output.utils import append_to_json, parse_openai_response, get_system_prompt_for_class

load_dotenv()

client = OpenAI(
    base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = "gpt-4o-mini"

def generate_response(class_name: str, response_format, n: int = 5):
    system_prompt, user_prompt = get_system_prompt_for_class(class_name)

    if not system_prompt or not user_prompt:
        raise ValueError(f"Aucun prompt valide trouvé pour {class_name}.")

    # Formatage du prompt utilisateur
    user_prompt = user_prompt.replace("{n}", str(n))

    # Appel à OpenAI
    response = client.beta.chat.completions.parse(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format=response_format,
    )

    return response

