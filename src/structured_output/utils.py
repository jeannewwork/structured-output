
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


def get_system_prompt_for_class(class_name: str, prompts_file: str = "system_prompts.json") -> str:
    try:
        with open(prompts_file, "r", encoding="utf-8") as file:
            prompts = json.load(file)

        if class_name in prompts:
            return prompts[class_name]  # Retourne le prompt système
        else:
            print(f"⚠️ Avertissement : Aucun prompt système trouvé pour la classe {class_name}.")
            return ""
    except FileNotFoundError:
        print(f" Erreur : Le fichier {prompts_file} est introuvable.")
        return ""
    except json.JSONDecodeError:
        print(f" Erreur : Le fichier {prompts_file} contient un JSON invalide.")
        return ""
    except Exception as e:
        print(f" Erreur inattendue : {e}")
        return ""

def get_associated_tables(class_name: str, associations_file: str = "table_associations.json") -> list:
    try:
        with open(associations_file, "r", encoding="utf-8") as file:
            associations = json.load(file)

        return associations.get(class_name, [])
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {associations_file} est introuvable.")
        return []
    except json.JSONDecodeError:
        print(f"❌ Erreur : Le fichier {associations_file} contient un JSON invalide.")
        return []
    except Exception as e:
        print(f"❌ Erreur inattendue : {e}")
        return []