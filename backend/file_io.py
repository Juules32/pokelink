import json
import pickle
from typing import Any

def pickle_dump(data: Any, filename: str) -> None:
    with open(f"data/{filename}.pkl", "wb") as file:
        pickle.dump(data, file)

def pickle_load(filename: str) -> Any:
    with open(f"data/{filename}.pkl", "rb") as file:
        return pickle.load(file)

def json_dump(data: Any, filename: str) -> None:
    with open(f"data/{filename}.json", "w") as file:
        json.dump(data, file, indent=4)

def json_load(filename: str) -> dict:
    with open(f"data/{filename}.json", "r") as file:
        return json.load(file)
