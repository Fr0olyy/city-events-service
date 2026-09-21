"""Тесты функций модуля registrations."""
import pytest

from registrations import (
    cancel_registration,
    create_registration,
    is_registration_open,
)


def test_is_registration_open_empty():
    assert is_registration_open([], 1)


def test_create_registration():
    registrations = []
    registration = create_registration(registrations, 1, "Иван")
    assert registration["id"] == 1
    assert len(registrations) == 1


def test_duplicate_registration_forbidden():
    registrations = []
    create_registration(registrations, 1, "Иван")
    with pytest.raises(ValueError):
        create_registration(registrations, 1, "Пётр")


def test_cancel_registration():
    registrations = []
    registration = create_registration(registrations, 1, "Иван")
    result = cancel_registration(registrations, registration["id"])
    assert result is True
    assert registrations == []


def test_cancel_missing_registration():
    assert cancel_registration([], 999) is False
