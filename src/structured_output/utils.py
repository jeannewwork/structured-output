
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


def get_system_prompt_for_class(class_name: str, prompts_file: str = "/Users/datacraft/structured-output/data/system_prompt.json") -> str:
    with open(prompts_file, "r", encoding="utf-8") as file:
        prompts = json.load(file)

    if class_name in prompts:
        return prompts[class_name]  # Retourne le prompt système
    else:
        print(f"Aucun prompt système trouvé pour la classe {class_name}.")
        return ""

def get_associated_tables(class_name: str, associations_file: str = "/Users/datacraft/structured-output/data/table_association.json") -> list:
    with open(associations_file, "r", encoding="utf-8") as file:
        associations = json.load(file)

    return associations.get(class_name, [])

    
def load_existing_data(tables: list, data_path: str = "/Users/datacraft/structured-output/data/") -> dict:
    """
    Charge les données existantes des tables associées.

    Args:
        tables (list): Liste des tables à charger.
        data_path (str): Chemin vers le dossier contenant les fichiers JSON des bases.

    Returns:
        dict: Un dictionnaire contenant les données chargées par table.
    """
    data = {}

    for table in tables:
        file_path = f"{data_path}{table.lower()}.json"

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read().strip()  # Lire et supprimer les espaces vides
                
                if not content:  # 📌 Vérifie si le fichier est vide
                    print(f"⚠️ Avertissement : {file_path} est vide. Initialisation d'une liste vide.")
                    data[table] = []
                else:
                    data[table] = json.loads(content)  # Charger les données si le fichier n'est pas vide

        except FileNotFoundError:
            print(f"⚠️ Avertissement : Le fichier {file_path} est introuvable. Initialisation d'une liste vide.")
            data[table] = []
        except json.JSONDecodeError:
            print(f"❌ Erreur : Le fichier {file_path} contient un JSON invalide. Vérifie son format.")
            data[table] = []
        except Exception as e:
            print(f"❌ Erreur inattendue pour {file_path} : {e}")
            data[table] = []

    return data

def get_user_prompt_system(prompt_file: str = "/Users/datacraft/structured-output/data/prompt_system_2.json") -> str:
    with open(prompt_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data.get("system", "")

def get_data(data_path, obj_id):
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            database = json.load(file)

        obj_to_complete = next((item for item in database if item["id"] == obj_id), None)

        if not obj_to_complete:
            raise ValueError(f"Aucune donnée trouvée pour ID {obj_id} dans {data_path}")

    except FileNotFoundError:
        raise FileNotFoundError(f"Erreur : Le fichier {data_path} est introuvable.")
    except json.JSONDecodeError:
        raise ValueError(f"Erreur : Le fichier {data_path} contient un JSON invalide.")