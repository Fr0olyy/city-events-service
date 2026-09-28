"""Тесты функций модуля storage."""
import os
import tempfile
from datetime import date

import storage
from models import Category, Event, Place, Registration, User
from storage import load_json, save_json


def test_save_and_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "test.json")
        data = {"1": {"id": 1, "name": "Тест"}}
        save_json(path, data)
        loaded = load_json(path, {})
        assert loaded == data


def test_load_missing_file_returns_default():
    assert load_json("no_such_file.json", {}) == {}


def test_load_corrupted_file_returns_default():
    with tempfile.TemporaryDirectory() as tmp:
        path = os.path.join(tmp, "bad.json")
        with open(path, "w", encoding="utf-8") as file:
            file.write("{not valid json")
        assert load_json(path, []) == []


def test_object_model_json_roundtrip(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        monkeypatch.setattr(storage, "DATA_PLACES", os.path.join(tmp, "places.json"))
        monkeypatch.setattr(
            storage, "DATA_CATEGORIES", os.path.join(tmp, "categories.json")
        )
        monkeypatch.setattr(storage, "DATA_EVENTS", os.path.join(tmp, "events.json"))
        monkeypatch.setattr(storage, "DATA_USERS", os.path.join(tmp, "users.json"))
        monkeypatch.setattr(
            storage,
            "DATA_REGISTRATIONS",
            os.path.join(tmp, "registrations.json"),
        )

        place = Place(1, "Филармония", "ул. Ленина, 5")
        category = Category(1, "концерт", "Музыка")
        event = Event(1, "Джаз", place, category, date(2026, 9, 15))
        user = User(1, "Борис")
        registration = Registration(1, event, user)

        storage.save_all_data(
            [place], [category], [event], [user], [registration]
        )
        places, categories, events, users, registrations = storage.load_all_data()

        assert places[0].name == "Филармония"
        assert events[0].place is places[0]
        assert events[0].category is categories[0]
        assert registrations[0].event is events[0]
        assert registrations[0].user is users[0]
        assert events[0].event_date == date(2026, 9, 15)


def test_legacy_json_records_are_loaded_into_objects(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        paths = {
            "DATA_PLACES": os.path.join(tmp, "places.json"),
            "DATA_CATEGORIES": os.path.join(tmp, "categories.json"),
            "DATA_EVENTS": os.path.join(tmp, "events.json"),
            "DATA_USERS": os.path.join(tmp, "users.json"),
            "DATA_REGISTRATIONS": os.path.join(tmp, "registrations.json"),
        }
        for name, path in paths.items():
            monkeypatch.setattr(storage, name, path)

        save_json(paths["DATA_PLACES"], {"1": {"id": 1, "name": "Парк", "address": "Центр"}})
        save_json(
            paths["DATA_CATEGORIES"],
            {"1": {"id": 1, "name": "концерт", "description": ""}},
        )
        save_json(
            paths["DATA_EVENTS"],
            {
                "1": {
                    "id": 1,
                    "title": "Джаз",
                    "place_id": 1,
                    "category_id": 3,
                    "event_date": "2026-09-15",
                }
            },
        )
        save_json(
            paths["DATA_REGISTRATIONS"],
            [{"id": 1, "event_id": 1, "user_name": "Борис"}],
        )

        places, categories, events, users, registrations = storage.load_all_data()
        assert places[0].name == "Парк"
        assert events[0].place is places[0]
        assert events[0].category is categories[-1]
        assert events[0].category.id == 3
        assert users[0].name == "Борис"
        assert registrations[0].user is users[0]
