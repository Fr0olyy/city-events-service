"""Модель городского события."""

from datetime import date

from .categories import Category
from .places import Place


class Event:
    """Событие с датой, местом проведения и категорией."""

    def __init__(
        self,
        event_id: int,
        title: str,
        place: Place,
        category: Category,
        event_date: date,
    ) -> None:
        self.id = event_id
        self.title = title
        self.place = place
        self.category = category
        self.event_date = event_date

    @classmethod
    def from_data(
        cls,
        data: dict,
        place: Place,
        category: Category,
    ) -> "Event":
        """Создать событие из JSON и связанных объектов."""
        event_date = data["event_date"]
        if isinstance(event_date, str):
            event_date = date.fromisoformat(event_date)
        return cls(data["id"], data["title"], place, category, event_date)

    def get_status(self, today: date | None = None) -> str:
        """Вернуть текстовый статус события относительно выбранной даты."""
        current_date = today or date.today()
        if self.event_date < current_date:
            return "Событие уже прошло"
        if self.event_date == current_date:
            return "Событие проходит сегодня"
        days_left = (self.event_date - current_date).days
        return f"До события осталось дней: {days_left}"

    def __str__(self) -> str:
        return (
            f"{self.title} | {self.event_date.isoformat()} | "
            f"{self.place.name} | {self.category.name}"
        )
