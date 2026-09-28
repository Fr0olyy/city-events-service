"""Модель категории городского события."""


class Category:
    """Категория для группировки городских событий."""

    def __init__(
        self,
        category_id: int,
        name: str,
        description: str = "",
    ) -> None:
        self.id = category_id
        self.name = name
        self.description = description

    @classmethod
    def from_data(cls, data: dict) -> "Category":
        """Создать категорию из записи JSON."""
        return cls(
            data["id"], data["name"], data.get("description", "")
        )

    def __str__(self) -> str:
        if self.description:
            return f"{self.name} — {self.description}"
        return self.name
