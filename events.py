"""Функции для работы с городскими событиями."""
from datetime import date


def add_event(
    events: dict[int, dict],
    title: str,
    place_id: int,
    category_id: int,
    event_date: date,
) -> int:
    """Добавить событие и вернуть его id."""
    new_id = max(events.keys(), default=0) + 1
    events[new_id] = {
        "id": new_id,
        "title": title,
        "place_id": place_id,
        "category_id": category_id,
        "event_date": event_date.isoformat(),
    }
    return new_id


def find_events(
    events: dict[int, dict],
    query: str,
) -> list[dict]:
    """Найти события по подстроке в названии."""
    query = query.lower()
    result = []
    for event in events.values():
        if query in event["title"].lower():
            result.append(event)
    return result


def filter_events_by_category(
    events: dict[int, dict],
    category_id: int,
) -> list[dict]:
    """Отобрать события по id категории."""
    result = []
    for event in events.values():
        if event["category_id"] == category_id:
            result.append(event)
    return result


def filter_events_by_date(
    events: dict[int, dict],
    on_date: date,
) -> list[dict]:
    """Отобрать события на конкретную дату."""
    iso = on_date.isoformat()
    result = []
    for event in events.values():
        if event["event_date"] == iso:
            result.append(event)
    return result


def sort_events_by_date(
    events: dict[int, dict],
) -> list[dict]:
    """Отсортировать события по дате."""
    return sorted(events.values(), key=lambda e: e["event_date"])


def get_event_status(event_date: date) -> str:
    """Вернуть текстовый статус события относительно сегодняшней даты.

    Функция перенесена из ПР1 и сохранена без изменений.
    """
    today = date.today()
    if event_date < today:
        return "Событие уже прошло"
    if event_date == today:
        return "Событие проходит сегодня"
    days_left = (event_date - today).days
    return f"До события осталось дней: {days_left}"


def show_events(events: dict[int, dict]) -> None:
    """Вывести список событий, отсортированных по дате."""
    if not events:
        print("Событий пока нет.")
        return
    for event in sort_events_by_date(events):
        print(
            f"[{event['id']}] {event['title']} | "
            f"{event['event_date']} | "
            f"место={event['place_id']} "
            f"кат={event['category_id']}"
        )
