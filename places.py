"""Функции для работы с местами проведения событий."""


def add_place(
    places: dict[int, dict],
    name: str,
    address: str,
) -> int:
    """Добавить место в словарь places и вернуть его id."""
    new_id = max(places.keys(), default=0) + 1
    places[new_id] = {
        "id": new_id,
        "name": name,
        "address": address,
    }
    return new_id


def find_places(
    places: dict[int, dict],
    query: str,
) -> list[dict]:
    """Найти места по подстроке в названии или адресе."""
    query = query.lower()
    result = []
    for place in places.values():
        if query in place["name"].lower():
            result.append(place)
        elif query in place["address"].lower():
            result.append(place)
    return result


def sort_places_by_name(
    places: dict[int, dict],
) -> list[dict]:
    """Отсортировать места по названию."""
    return sorted(places.values(), key=lambda p: p["name"])


def show_places(places: dict[int, dict]) -> None:
    """Вывести список мест в консоль."""
    if not places:
        print("Мест пока нет.")
        return
    for place in sort_places_by_name(places):
        print(f"[{place['id']}] {place['name']} — {place['address']}")
