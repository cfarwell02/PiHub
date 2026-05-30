import json
import os

SETTINGS_FILE = os.path.join("data", "settings.json")

DEFAULT_SETTINGS = {
    "auto_refresh": True,
    "refresh_interval": 1000,
    "temperature_unit": "C"
}

VALID_REFRESH_INTERVALS = [1000, 3000, 5000, 10000]
VALID_TEMPERATURE_UNITS = ["C", "F"]


def ensure_settings_file():
    os.makedirs("data", exist_ok=True)

    if not os.path.exists(SETTINGS_FILE):
        save_settings(DEFAULT_SETTINGS)


def load_settings():
    ensure_settings_file()

    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
    except json.JSONDecodeError:
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    return validate_settings(settings)


def save_settings(settings):
    os.makedirs("data", exist_ok=True)

    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=2)


def validate_settings(settings):
    validated_settings = DEFAULT_SETTINGS.copy()

    refresh_interval = settings.get("refresh_interval", DEFAULT_SETTINGS["refresh_interval"])
    temperature_unit = settings.get("temperature_unit", DEFAULT_SETTINGS["temperature_unit"])
    auto_refresh = settings.get("auto_refresh", DEFAULT_SETTINGS["auto_refresh"])

    try:
        refresh_interval = int(refresh_interval)
    except (TypeError, ValueError):
        refresh_interval = DEFAULT_SETTINGS["refresh_interval"]

    if refresh_interval not in VALID_REFRESH_INTERVALS:
        refresh_interval = DEFAULT_SETTINGS["refresh_interval"]

    if temperature_unit not in VALID_TEMPERATURE_UNITS:
        temperature_unit = DEFAULT_SETTINGS["temperature_unit"]

    if not isinstance(auto_refresh, bool):
        auto_refresh = DEFAULT_SETTINGS["auto_refresh"]

    validated_settings["refresh_interval"] = refresh_interval
    validated_settings["temperature_unit"] = temperature_unit
    validated_settings["auto_refresh"] = auto_refresh

    return validated_settings


def update_settings(new_settings):
    current_settings = load_settings()
    updated_settings = current_settings.copy()

    updated_settings.update(new_settings)

    validated_settings = validate_settings(updated_settings)

    save_settings(validated_settings)

    return validated_settings