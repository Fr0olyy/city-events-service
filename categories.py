"""Функции для работы с категориями событий."""


def add_category(
    categories: dict[int, dict],
    name: str,
    description: str = "",
) -> int:
    """Добавить категорию и вернуть её id."""
    new_id = max(categories.keys(), default=0) + 1
    categories[new_id] = {
        "id": new_id,
        "name": name,
        "description": description,
    }
    return new_id


def find_category_by_name(
    categories: dict[int, dict],
    name: str,
) -> dict | None:
    """Найти категорию по точному названию (без учёта регистра)."""
    name = name.lower()
    for category in categories.values():
        if category["name"].lower() == name:
            return category
    return None


def list_category_names(
    categories: dict[int, dict],
) -> list[str]:
    """Вернуть список названий категорий."""
    return [c["name"] for c in categories.values()]


def show_categories(categories: dict[int, dict]) -> None:
    """Вывести список категорий в консоль."""
    if not categories:
        print("Категорий пока нет.")
        return
    for category in categories.values():
        print(
            f"[{category['id']}] {category['name']} — "
            f"{category['description']}"
        )
