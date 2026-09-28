"""Модель пользователя сервиса городских событий."""


class User:
    """Участник, который может зарегистрироваться на событие."""

    def __init__(self, user_id: int, name: str) -> None:
        self.id = user_id
        self.name = name

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из записи JSON."""
        return cls(data["id"], data["name"])

    def __str__(self) -> str:
        return self.name
