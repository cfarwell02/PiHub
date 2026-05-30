import json
import os

SETTINGS_FILE = os.path.join("data", "settings.json")

DEFAULT_SETTINGS = {
    "auto_refresh": True,
    "refresh_interval": 1000,
    "temperature_unit": "F"
}


def ensure_settings_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    ensure_settings_file()

    try:
        with open(SETTINGS_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS


def save_settings(settings):
    os.makedirs("data", exist_ok=True)

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


def update_settings(new_settings):
    settings = load_settings()

    settings.update(new_settings)

    save_settings(settings)

    return settings