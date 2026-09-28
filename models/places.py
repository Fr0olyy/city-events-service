"""Модель места проведения городского события."""


class Place:
    """Площадка, на которой проводятся городские события."""

    def __init__(self, place_id: int, name: str, address: str) -> None:
        self.id = place_id
        self.name = name
        self.address = address

    @classmethod
    def from_data(cls, data: dict) -> "Place":
        """Создать место из записи JSON."""
        return cls(data["id"], data["name"], data["address"])

    def __str__(self) -> str:
        return f"{self.name} — {self.address}"
