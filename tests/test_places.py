"""Тесты объектной модели мест."""

from models import Place
from places import add_place, find_places, sort_places_by_name


def test_place_creation_and_string_representation():
    place = Place(1, "Филармония", "ул. Ленина, 5")
    assert place.id == 1
    assert place.name == "Филармония"
    assert str(place) == "Филармония — ул. Ленина, 5"


def test_add_place_returns_and_stores_object():
    places = [Place(3, "Парк", "Крымский Вал")]
    place = add_place(places, "Филармония", "ул. Ленина, 5")
    assert place.id == 4
    assert places[-1] is place


def test_find_places_by_name_and_address():
    places = [
        Place(1, "Филармония", "ул. Ленина, 5"),
        Place(2, "Парк Горького", "Крымский Вал, 9"),
    ]
    assert find_places(places, "филарм") == [places[0]]
    assert find_places(places, "ленина") == [places[0]]


def test_sort_places_by_name():
    places = [
        Place(1, "Филармония", "ул. Ленина, 5"),
        Place(2, "Арена", "Спортивная, 1"),
    ]
    assert [place.name for place in sort_places_by_name(places)] == [
        "Арена",
        "Филармония",
    ]
