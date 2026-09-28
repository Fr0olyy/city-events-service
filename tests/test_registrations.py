"""Тесты объектной модели регистраций."""

from datetime import date

import pytest

from models import Category, Event, Place, Registration, User
from registrations import (
    cancel_registration,
    create_registration,
    is_registration_open,
)


def _event() -> Event:
    return Event(
        1,
        "Джаз",
        Place(1, "Филармония", "ул. Ленина, 5"),
        Category(1, "концерт"),
        date(2026, 9, 15),
    )


def test_registration_links_user_and_event_objects():
    registrations: list[Registration] = []
    event = _event()
    user = User(1, "Иван")
    registration = create_registration(registrations, event, user)
    assert registration.event is event
    assert registration.user is user
    assert registration.id == 1
    assert registrations == [registration]
    assert "Иван" in str(registration)


def test_duplicate_active_registration_forbidden():
    registrations: list[Registration] = []
    event = _event()
    create_registration(registrations, event, User(1, "Иван"))
    assert not is_registration_open(registrations, event)
    with pytest.raises(ValueError):
        create_registration(registrations, event, User(2, "Пётр"))


def test_cancel_registration_keeps_history_and_reopens_event():
    registrations: list[Registration] = []
    event = _event()
    registration = create_registration(
        registrations, event, User(1, "Иван")
    )
    assert cancel_registration(registrations, registration.id)
    assert registrations == [registration]
    assert registration.is_cancelled
    assert is_registration_open(registrations, event)
    create_registration(registrations, event, User(2, "Пётр"))
    assert len(registrations) == 2


def test_cancel_missing_or_already_cancelled_registration():
    registrations: list[Registration] = []
    assert not cancel_registration(registrations, 999)
    registration = create_registration(
        registrations, _event(), User(1, "Иван")
    )
    assert cancel_registration(registrations, registration.id)
    assert not cancel_registration(registrations, registration.id)
