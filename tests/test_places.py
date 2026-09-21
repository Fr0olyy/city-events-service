"""Тесты функций модуля places."""
from places import add_place, find_places, sort_places_by_name


def test_add_place_returns_id():
    places = {}
    place_id = add_place(places, "Филармония", "ул. Ленина, 5")
    assert place_id == 1
    assert len(places) == 1


def test_add_place_increments_id():
    places = {}
    add_place(places, "Филармония", "ул. Ленина, 5")
    place_id = add_place(places, "Парк", "Крымский Вал, 9")
    assert place_id == 2


def test_find_places_by_name():
    places = {}
    add_place(places, "Филармония", "ул. Ленина, 5")
    add_place(places, "Парк Горького", "Крымский Вал, 9")
    found = find_places(places, "филарм")
    assert len(found) == 1
    assert found[0]["name"] == "Филармония"


def test_find_places_by_address():
    places = {}
    add_place(places, "Филармония", "ул. Ленина, 5")
    found = find_places(places, "ленина")
    assert len(found) == 1


def test_sort_places_by_name():
    places = {}
    add_place(places, "Филармония", "ул. Ленина, 5")
    add_place(places, "Арена", "спортивная, 1")
    names = [p["name"] for p in sort_places_by_name(places)]
    assert names == ["Арена", "Филармония"]
