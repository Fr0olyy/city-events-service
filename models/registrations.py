"""Модель регистрации пользователя на событие."""

from .events import Event
from .users import User


class Registration:
    """Регистрация связывает пользователя с выбранным событием."""

    def __init__(
        self,
        registration_id: int,
        event: Event,
        user: User,
        is_cancelled: bool = False,
    ) -> None:
        self.id = registration_id
        self.event = event
        self.user = user
        self._is_cancelled = is_cancelled

    @property
    def is_cancelled(self) -> bool:
        """Текущее состояние регистрации (доступно только для чтения)."""
        return self._is_cancelled

    def cancel(self) -> None:
        """Отменить регистрацию, сохранив её в истории."""
        self._is_cancelled = True

    def __str__(self) -> str:
        status = "отменена" if self.is_cancelled else "активна"
        return (
            f"Регистрация {self.id}: {self.user.name} — "
            f"{self.event.title} ({status})"
        )
