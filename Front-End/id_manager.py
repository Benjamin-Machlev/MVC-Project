import json
import os

ID_FILE_PATH = "current_id.json"

def load_current_id():
    if os.path.exists(ID_FILE_PATH):
        with open(ID_FILE_PATH, "r") as file:
            data = json.load(file)
            return data.get("current_movie_id", 17)
    return 17

def save_current_id(current_id):
    with open(ID_FILE_PATH, "w") as file:
        json.dump({"current_movie_id": current_id}, file)
    print(f"Saved current_movie_id: {current_id} to {ID_FILE_PATH}")  # Debug print