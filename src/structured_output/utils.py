
import json
from typing import Type, List
from pydantic import BaseModel


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


def parse_openai_response(response, model: Type[BaseModel]) -> List[BaseModel]:

    new_data = response.choices[0].message.content

    if isinstance(new_data, str):
        new_data = json.loads(new_data)

    if isinstance(new_data, dict): 
        new_data = [new_data]  

    return [model(**item) for item in new_data]