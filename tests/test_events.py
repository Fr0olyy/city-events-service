"""Тесты функций модуля events."""
from datetime import date

from events import (
    add_event,
    filter_events_by_category,
    filter_events_by_date,
    find_events,
    get_event_status,
)


def test_add_event_returns_id():
    events = {}
    event_id = add_event(events, "Джаз", 1, 1, date(2026, 9, 15))
    assert event_id == 1
    assert events[1]["event_date"] == "2026-09-15"


def test_find_events_by_title():
    events = {}
    add_event(events, "Джазовый концерт", 1, 1, date(2026, 9, 15))
    add_event(events, "Рок-фестиваль", 1, 1, date(2026, 9, 16))
    found = find_events(events, "джаз")
    assert len(found) == 1


def test_filter_events_by_date():
    events = {}
    add_event(events, "Джаз", 1, 1, date(2026, 9, 15))
    add_event(events, "Рок", 1, 1, date(2026, 9, 16))
    found = filter_events_by_date(events, date(2026, 9, 15))
    assert len(found) == 1
    assert found[0]["title"] == "Джаз"


def test_filter_events_by_category():
    events = {}
    add_event(events, "Джаз", 1, 1, date(2026, 9, 15))
    add_event(events, "Выставка", 1, 2, date(2026, 9, 16))
    found = filter_events_by_category(events, 1)
    assert len(found) == 1


def test_get_event_status_past():
    assert get_event_status(date(2020, 1, 1)) == "Событие уже прошло"


def test_get_event_status_future():
    status = get_event_status(date(2099, 1, 1))
    assert status.startswith("До события осталось дней:")
