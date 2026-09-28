"""Операции над коллекцией городских событий."""

from datetime import date

from models import Category, Event, Place


def add_event(
    events: list[Event],
    title: str,
    place: Place,
    category: Category,
    event_date: date,
) -> Event:
    """Создать событие, добавить его в коллекцию и вернуть объект."""
    new_id = max((event.id for event in events), default=0) + 1
    event = Event(new_id, title, place, category, event_date)
    events.append(event)
    return event


def find_events(events: list[Event], query: str) -> list[Event]:
    """Найти события по подстроке в названии."""
    normalized_query = query.casefold()
    return [
        event
        for event in events
        if normalized_query in event.title.casefold()
    ]


def filter_events_by_category(
    events: list[Event],
    category: Category | int,
) -> list[Event]:
    """Отобрать события по объекту категории или его идентификатору."""
    category_id = category.id if isinstance(category, Category) else category
    return [event for event in events if event.category.id == category_id]


def filter_events_by_date(events: list[Event], on_date: date) -> list[Event]:
    """Отобрать события на конкретную дату."""
    return [event for event in events if event.event_date == on_date]


def sort_events_by_date(events: list[Event]) -> list[Event]:
    """Вернуть события, отсортированные по дате."""
    return sorted(events, key=lambda event: (event.event_date, event.id))


def get_event_status(event_date: date) -> str:
    """Вернуть статус даты события относительно сегодняшнего дня."""
    today = date.today()
    if event_date < today:
        return "Событие уже прошло"
    if event_date == today:
        return "Событие проходит сегодня"
    days_left = (event_date - today).days
    return f"До события осталось дней: {days_left}"


def show_events(events: list[Event]) -> None:
    """Вывести список событий, отсортированных по дате."""
    if not events:
        print("Событий пока нет.")
        return
    for event in sort_events_by_date(events):
        print(f"[{event.id}] {event}")
