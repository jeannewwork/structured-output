import json
from typing import Dict, Any, Literal, List
from pydantic import BaseModel

def get_system_prompt_for_class(class_name: str, prompts_file: str = "/Users/datacraft/structured-output/data/system_prompt.json") -> str:
    with open(prompts_file, "r", encoding="utf-8") as file:
        prompts = json.load(file)

    if class_name in prompts:
        return prompts[class_name]  # Retourne le prompt système
    else:
        print(f"Aucun prompt système trouvé pour la classe {class_name}.")
        return ""

def get_data(data_path, obj_id):
    """
    Retrieves a specific object by its ID from a JSON file.

    Args:
        data_path (str): Path to the JSON database file.
        obj_id (int): The ID of the object to retrieve.

    Returns:
        Dict[str, Any]: The retrieved object.

    Raises:
        ValueError: If the object is not found.
    """
    try:
        with open(data_path, "r", encoding="utf-8") as file:
            database = json.load(file)

        obj_to_complete = database[obj_id-1] 
        

        if not obj_to_complete:
            raise ValueError(f"Aucune donnée trouvée pour ID {obj_id} dans {data_path}")
        else : 
            return obj_to_complete

    except FileNotFoundError:
        raise FileNotFoundError(f"Erreur : Le fichier {data_path} est introuvable.")
    except json.JSONDecodeError:
        raise ValueError(f"Erreur : Le fichier {data_path} contient un JSON invalide.")
    

def generate_user_prompt(obj_to_complete: Dict[str, Any]) -> str:
    """
    Constructs a user prompt for OpenAI to complete missing values in a given object.

    Args:
        obj_to_complete (Dict[str, Any]): The object with missing values.

    Returns:
        str: The formatted user prompt.
    """
    return (
        "Complete the following data while strictly preserving the existing values. "
        "Ensure that all present fields remain unchanged. "
        "Generate only the missing values in a coherent and contextually appropriate manner based on the provided information.\n\n"
        f"{json.dumps(obj_to_complete, indent=4, ensure_ascii=False)}"
    )

def save_data(data: list, data_path: str) -> None:
    """
    Saves a list of Pydantic objects to a JSON file.

    Args:
        data (list): The list of objects to save.
        data_path (str): The file path for the JSON file.
    """
    with open(data_path, "w", encoding="utf-8") as file:
        json.dump([item.model_dump() for item in data], file, indent=4, ensure_ascii=False, default=str)