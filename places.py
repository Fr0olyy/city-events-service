"""Операции над коллекцией мест проведения событий."""

from models import Place


def add_place(places: list[Place], name: str, address: str) -> Place:
    """Создать место, добавить его в коллекцию и вернуть объект."""
    new_id = max((place.id for place in places), default=0) + 1
    place = Place(new_id, name, address)
    places.append(place)
    return place


def find_places(places: list[Place], query: str) -> list[Place]:
    """Найти места по подстроке в названии или адресе."""
    normalized_query = query.casefold()
    return [
        place
        for place in places
        if normalized_query in place.name.casefold()
        or normalized_query in place.address.casefold()
    ]


def sort_places_by_name(places: list[Place]) -> list[Place]:
    """Вернуть места, отсортированные по названию."""
    return sorted(places, key=lambda place: place.name.casefold())


def show_places(places: list[Place]) -> None:
    """Вывести список мест в консоль."""
    if not places:
        print("Мест пока нет.")
        return
    for place in sort_places_by_name(places):
        print(f"[{place.id}] {place}")
