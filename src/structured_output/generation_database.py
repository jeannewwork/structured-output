import os
import json
from datetime import date
from openai import OpenAI
from dotenv import load_dotenv

from structured_output.class_database import Hotel, Room, Option, RoomOption, HotelOption, StayOption, Customer, Reservation

load_dotenv()

client = OpenAI(
    base_url="https://api.openai.com/v1", api_key=os.getenv("OPENAI_API_KEY")
)

MODEL_NAME = "gpt-4o-mini"

response = client.beta.chat.completions.parse(
    model=MODEL_NAME,
    messages=[
        {"role": "system", "content": "Génère {n} hôtels sous forme de JSON avec id, name, address, tag ('montagne', 'plage', 'ville', 'campagne'). "},
        {"role": "user", "content": "Voici un premier exemple : id=1, name=Hôtel du Lac, address=123 Rue des Alpes, Annecy, tag=montagne, tu peux changer les valeurs tant que tu respectes la structure"},
    ],
    response_format=Hotel,
)

def append_to_json(filename, new_data):
    try:
        
        with open(filename, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        
        existing_data = []

    existing_data.extend([item.dict() for item in new_data])
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    print(f"✅ {len(new_data)} nouveaux hôtels ajoutés à {filename}")