"""Загрузка и сохранение данных проекта в JSON-файлах."""
import json
import os


def load_json(filename: str, default):
    """Загрузить данные из JSON.

    Если файла нет или он повреждён — вернуть default.
    """
    if not os.path.exists(filename):
        return default
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as error:
        print(f"Ошибка чтения {filename}: {error}")
        return default


def save_json(filename: str, data) -> None:
    """Сохранить данные в JSON-файл."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
