import os
import json
from typing import Type, List
from pydantic import BaseModel
from datetime import date
from openai import OpenAI
from dotenv import load_dotenv

from structured_output.class_database import Hotel, Room, Option, RoomOption, HotelOption, StayOption, Customer, Reservation
from structured_output.utils import append_to_json, parse_openai_response

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

for i in range (5):
    new_hotels = parse_openai_response(response, Hotel)
    append_to_json("/Users/datacraft/structured-output/data/hotel.json", new_hotels)