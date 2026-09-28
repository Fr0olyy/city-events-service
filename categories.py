"""Операции над коллекцией категорий событий."""

from models import Category


def add_category(
    categories: list[Category],
    name: str,
    description: str = "",
) -> Category:
    """Создать категорию, добавить её в коллекцию и вернуть объект."""
    new_id = max((category.id for category in categories), default=0) + 1
    category = Category(new_id, name, description)
    categories.append(category)
    return category


def find_category_by_name(
    categories: list[Category],
    name: str,
) -> Category | None:
    """Найти категорию по точному названию без учёта регистра."""
    normalized_name = name.casefold()
    return next(
        (
            category
            for category in categories
            if category.name.casefold() == normalized_name
        ),
        None,
    )


def list_category_names(categories: list[Category]) -> list[str]:
    """Вернуть список названий категорий."""
    return [category.name for category in categories]


def show_categories(categories: list[Category]) -> None:
    """Вывести список категорий в консоль."""
    if not categories:
        print("Категорий пока нет.")
        return
    for category in categories:
        print(f"[{category.id}] {category}")
