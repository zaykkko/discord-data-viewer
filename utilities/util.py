import os
import json
from typing import Any

import settings


def load_json(json_path: str) -> Any:
    with open(json_path, encoding="utf8") as json_data:
        return json.load(json_data)


def get_channel_dir(base_dir: str, channel_id: str) -> str:
    return os.path.join(
        base_dir, settings.MESSAGES_DIR, settings.CHANNEL_PREFIX_FOLDER + channel_id
    )


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def press_any_key() -> None:
    input("Presiona cualquier tecla para continuar...")
