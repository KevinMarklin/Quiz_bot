import json
import os

LOCK_STATE_FILE = "lock_state.json"
DEFAULT_STATE = {"is_locked": True}

# Загружаем состояние из файла (или создаём с дефолтом)
def load_state():
    if not os.path.exists(LOCK_STATE_FILE):
        save_state(DEFAULT_STATE)
    with open(LOCK_STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state: dict):
    with open(LOCK_STATE_FILE, "w") as f:
        json.dump(state, f)

# Работа с флагом блокировки
def is_locked() -> bool:
    return load_state()["is_locked"]

def set_locked(value: bool):
    save_state({"is_locked": value})