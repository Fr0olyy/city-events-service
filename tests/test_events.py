"""Тесты объектной модели событий и функций работы с ними."""

from datetime import date

from categories import add_category
from events import (
    add_event,
    filter_events_by_category,
    filter_events_by_date,
    find_events,
    get_event_status,
    sort_events_by_date,
)
from models import Category, Event, Place


def _event(
    event_id: int,
    title: str,
    event_date: date,
    category: Category | None = None,
) -> Event:
    return Event(
        event_id,
        title,
        Place(1, "Филармония", "ул. Ленина, 5"),
        category or Category(1, "концерт"),
        event_date,
    )


def test_event_contains_related_objects_and_string():
    place = Place(1, "Филармония", "ул. Ленина, 5")
    category = Category(1, "концерт")
    event = Event(1, "Джаз", place, category, date(2026, 9, 15))
    assert event.place is place
    assert event.category is category
    assert str(event) == "Джаз | 2026-09-15 | Филармония | концерт"


def test_add_event_returns_and_stores_object():
    events: list[Event] = []
    place = Place(1, "Филармония", "ул. Ленина, 5")
    category = Category(1, "концерт")
    event = add_event(events, "Джаз", place, category, date(2026, 9, 15))
    assert event.id == 1
    assert events == [event]
    assert event.place is place


def test_find_events_by_title():
    events = [
        _event(1, "Джазовый концерт", date(2026, 9, 15)),
        _event(2, "Рок-фестиваль", date(2026, 9, 16)),
    ]
    assert find_events(events, "джаз") == [events[0]]


def test_filter_events_by_date_and_category():
    concert = Category(1, "концерт")
    exhibition = Category(2, "выставка")
    events = [
        _event(1, "Джаз", date(2026, 9, 15), concert),
        _event(2, "Экспозиция", date(2026, 9, 15), exhibition),
    ]
    assert filter_events_by_date(events, date(2026, 9, 15)) == events
    assert filter_events_by_category(events, concert) == [events[0]]
    assert filter_events_by_category(events, 2) == [events[1]]


def test_sort_events_by_date():
    events = [
        _event(1, "Позже", date(2026, 9, 16)),
        _event(2, "Раньше", date(2026, 9, 15)),
    ]
    assert [event.title for event in sort_events_by_date(events)] == [
        "Раньше",
        "Позже",
    ]


def test_event_statuses():
    event = _event(1, "Тест", date(2099, 1, 1))
    assert event.get_status(date(2098, 12, 31)) == (
        "До события осталось дней: 1"
    )
    assert event.get_status(date(2099, 1, 1)) == "Событие проходит сегодня"
    assert event.get_status(date(2100, 1, 1)) == "Событие уже прошло"


def test_get_event_status_compatibility_function():
    assert get_event_status(date(2020, 1, 1)) == "Событие уже прошло"
    assert get_event_status(date(2099, 1, 1)).startswith(
        "До события осталось дней:"
    )


def test_add_category_creates_object():
    categories: list[Category] = []
    category = add_category(categories, "концерт", "Музыка")
    assert category.id == 1
    assert categories[0] is category
    assert str(category) == "концерт — Музыка"
