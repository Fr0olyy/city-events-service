"""Преобразование объектной модели в JSON и обратно."""
import json
import os
from typing import Any

from models import Category, Event, Place, Registration, User

DATA_PLACES = "data/places.json"
DATA_CATEGORIES = "data/categories.json"
DATA_EVENTS = "data/events.json"
DATA_USERS = "data/users.json"
DATA_REGISTRATIONS = "data/registrations.json"


def load_json(filename: str, default: Any) -> Any:
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


def save_json(filename: str, data: Any) -> None:
    """Сохранить данные в JSON-файл."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def _records(data: Any) -> list[dict]:
    """Нормализовать старый формат словаря и новый формат списка."""
    if isinstance(data, dict):
        return list(data.values())
    if isinstance(data, list):
        return data
    return []


def _by_id(objects: list[Any]) -> dict[int, Any]:
    return {item.id: item for item in objects}


def load_all_data(
) -> tuple[
    list[Place],
    list[Category],
    list[Event],
    list[User],
    list[Registration],
]:
    """Загрузить сущности и восстановить связи между объектами."""
    places = [
        Place.from_data(item) for item in _records(load_json(DATA_PLACES, []))
    ]
    categories = [
        Category.from_data(item)
        for item in _records(load_json(DATA_CATEGORIES, []))
    ]
    place_by_id = _by_id(places)
    category_by_id = _by_id(categories)

    events: list[Event] = []
    for item in _records(load_json(DATA_EVENTS, [])):
        place = place_by_id.get(item.get("place_id"))
        category_id = item.get("category_id")
        category = category_by_id.get(category_id)
        if place is None:
            print(f"Событие {item.get('id')} пропущено: место не найдено.")
            continue
        if category is None and category_id is not None:
            category = Category(
                category_id,
                f"Категория {category_id}",
                "Восстановлена из записи события",
            )
            categories.append(category)
            category_by_id[category.id] = category
            print(
                f"Для события {item.get('id')} создана категория-заглушка "
                f"с id={category.id}."
            )
        if category is None:
            print(f"Событие {item.get('id')} пропущено: категория не найдена.")
            continue
        events.append(Event.from_data(item, place, category))
    event_by_id = _by_id(events)

    users = [
        User.from_data(item) for item in _records(load_json(DATA_USERS, []))
    ]
    user_by_id = _by_id(users)
    user_by_name = {user.name.casefold(): user for user in users}

    registrations: list[Registration] = []
    registration_data = _records(load_json(DATA_REGISTRATIONS, []))
    for item in registration_data:
        event = event_by_id.get(item.get("event_id"))
        if event is None:
            print(
                f"Регистрация {item.get('id')} пропущена: событие не найдено."
            )
            continue

        user_id = item.get("user_id")
        user = user_by_id.get(user_id) if user_id is not None else None
        if user is None:
            user_name = item.get("user_name", "Неизвестный пользователь")
            user = user_by_name.get(user_name.casefold())
            if user is None:
                new_id = max((registered.id for registered in users), default=0) + 1
                user = User(new_id, user_name)
                users.append(user)
                user_by_id[user.id] = user
                user_by_name[user.name.casefold()] = user
        registrations.append(
            Registration(
                item["id"],
                event,
                user,
                item.get("is_cancelled", False),
            )
        )

    return places, categories, events, users, registrations


def save_all_data(
    places: list[Place],
    categories: list[Category],
    events: list[Event],
    users: list[User],
    registrations: list[Registration],
) -> None:
    """Сохранить объекты в совместимый JSON-формат с внешними id-ссылками."""
    save_json(
        DATA_PLACES,
        {
            str(place.id): {
                "id": place.id,
                "name": place.name,
                "address": place.address,
            }
            for place in places
        },
    )
    save_json(
        DATA_CATEGORIES,
        {
            str(category.id): {
                "id": category.id,
                "name": category.name,
                "description": category.description,
            }
            for category in categories
        },
    )
    save_json(
        DATA_EVENTS,
        {
            str(event.id): {
                "id": event.id,
                "title": event.title,
                "place_id": event.place.id,
                "category_id": event.category.id,
                "event_date": event.event_date.isoformat(),
            }
            for event in events
        },
    )
    save_json(
        DATA_USERS,
        {
            str(user.id): {"id": user.id, "name": user.name}
            for user in users
        },
    )
    save_json(
        DATA_REGISTRATIONS,
        [
            {
                "id": registration.id,
                "event_id": registration.event.id,
                "user_id": registration.user.id,
                "user_name": registration.user.name,
                "is_cancelled": registration.is_cancelled,
            }
            for registration in registrations
        ],
    )
