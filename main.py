"""Точка запуска приложения «Сервис учета городских событий»."""

from datetime import date

from categories import add_category, show_categories
from events import (
    add_event,
    filter_events_by_date,
    find_events,
    show_events,
)
from models import Category, Event, Place, Registration, User
from places import add_place, find_places, show_places
from registrations import (
    cancel_registration,
    create_registration,
    is_registration_open,
    show_registrations,
)
from storage import load_all_data, save_all_data
from utils import input_date, input_int, input_str


def print_menu() -> None:
    """Вывести меню приложения."""
    print("\n=== Сервис учета городских событий ===")
    print("1. Показать события")
    print("2. Показать места")
    print("3. Показать категории")
    print("4. Найти место")
    print("5. Добавить место")
    print("6. Добавить категорию")
    print("7. Добавить событие")
    print("8. Найти событие")
    print("9. Показать события на дату")
    print("10. Зарегистрироваться на событие")
    print("11. Показать регистрации")
    print("12. Отменить регистрацию")
    print("0. Выход")


def handle_find_place(places: list[Place]) -> None:
    """Обработать поиск места по подстроке."""
    if not places:
        print("Мест пока нет.")
        return
    found = find_places(places, input_str("Подстрока названия или адреса: "))
    if not found:
        print("Ничего не найдено.")
        return
    for place in found:
        print(f"[{place.id}] {place}")


def handle_add_place(places: list[Place]) -> None:
    """Обработать добавление места."""
    place = add_place(
        places,
        input_str("Название места: "),
        input_str("Адрес: "),
    )
    print(f"Место добавлено, id={place.id}")


def handle_add_category(categories: list[Category]) -> None:
    """Обработать добавление категории."""
    name = input_str("Название категории: ")
    description = input("Описание (необязательно): ").strip()
    category = add_category(categories, name, description)
    print(f"Категория добавлена, id={category.id}")


def _find_place(places: list[Place], place_id: int) -> Place | None:
    return next((place for place in places if place.id == place_id), None)


def _find_category(
    categories: list[Category],
    category_id: int,
) -> Category | None:
    return next(
        (category for category in categories if category.id == category_id),
        None,
    )


def _find_event(events: list[Event], event_id: int) -> Event | None:
    return next((event for event in events if event.id == event_id), None)


def handle_add_event(
    events: list[Event],
    places: list[Place],
    categories: list[Category],
) -> None:
    """Обработать добавление события с объектами места и категории."""
    if not places:
        print("Сначала добавьте хотя бы одно место.")
        return
    if not categories:
        print("Сначала добавьте хотя бы одну категорию.")
        return

    title = input_str("Название события: ")
    show_places(places)
    place = _find_place(places, input_int("id места: "))
    if place is None:
        print("Место с таким id не найдено.")
        return

    show_categories(categories)
    category = _find_category(categories, input_int("id категории: "))
    if category is None:
        print("Категория с таким id не найдена.")
        return

    event_date = date.fromisoformat(input_date("Дата (ДД.ММ.ГГГГ): "))
    event = add_event(events, title, place, category, event_date)
    print(f"Событие добавлено, id={event.id}")


def handle_find_event(events: list[Event]) -> None:
    """Обработать поиск события по названию."""
    found = find_events(events, input_str("Подстрока названия: "))
    if not found:
        print("Ничего не найдено.")
        return
    for event in found:
        print(f"[{event.id}] {event}")


def handle_events_on_date(events: list[Event]) -> None:
    """Показать события на выбранную дату и их статус."""
    on_date = date.fromisoformat(input_date("Дата (ДД.ММ.ГГГГ): "))
    found = filter_events_by_date(events, on_date)
    if not found:
        print("На эту дату событий нет.")
        return
    for event in found:
        print(f"[{event.id}] {event.title} | {event.get_status()}")


def _get_or_create_user(users: list[User], name: str) -> User:
    user = next(
        (person for person in users if person.name.casefold() == name.casefold()),
        None,
    )
    if user is not None:
        return user
    user_id = max((person.id for person in users), default=0) + 1
    user = User(user_id, name)
    users.append(user)
    return user


def handle_create_registration(
    registrations: list[Registration],
    events: list[Event],
    users: list[User],
) -> None:
    """Обработать создание регистрации на выбранное событие."""
    if not events:
        print("Событий пока нет.")
        return
    show_events(events)
    event = _find_event(events, input_int("id события: "))
    if event is None:
        print("Событие с таким id не найдено.")
        return
    if not is_registration_open(registrations, event):
        print("Ошибка: регистрация на это событие уже существует")
        return
    user = _get_or_create_user(users, input_str("Ваше имя: "))
    try:
        registration = create_registration(registrations, event, user)
        print(f"Регистрация создана, id={registration.id}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def handle_cancel_registration(registrations: list[Registration]) -> None:
    """Обработать отмену регистрации."""
    if not registrations:
        print("Регистраций пока нет.")
        return
    show_registrations(registrations)
    registration_id = input_int("id регистрации: ")
    if cancel_registration(registrations, registration_id):
        print("Регистрация отменена.")
    else:
        print("Активная регистрация с таким id не найдена.")


def main() -> None:
    """Загрузить данные, запустить меню и сохранить изменения."""
    places, categories, events, users, registrations = load_all_data()

    while True:
        print_menu()
        choice = input_int("Выберите действие: ")

        if choice == 0:
            break
        if choice == 1:
            show_events(events)
        elif choice == 2:
            show_places(places)
        elif choice == 3:
            show_categories(categories)
        elif choice == 4:
            handle_find_place(places)
        elif choice == 5:
            handle_add_place(places)
        elif choice == 6:
            handle_add_category(categories)
        elif choice == 7:
            handle_add_event(events, places, categories)
        elif choice == 8:
            handle_find_event(events)
        elif choice == 9:
            handle_events_on_date(events)
        elif choice == 10:
            handle_create_registration(registrations, events, users)
        elif choice == 11:
            show_registrations(registrations)
        elif choice == 12:
            handle_cancel_registration(registrations)
        else:
            print("Неизвестная команда, попробуйте снова.")

    save_all_data(places, categories, events, users, registrations)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
