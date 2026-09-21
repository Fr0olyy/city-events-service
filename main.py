"""Точка запуска приложения «Сервис учета городских событий»."""
from datetime import date

from categories import add_category, show_categories
from events import (
    add_event,
    filter_events_by_date,
    find_events,
    get_event_status,
    show_events,
)
from places import add_place, find_places, show_places
from registrations import (
    cancel_registration,
    create_registration,
    show_registrations,
)
from storage import load_json, save_json
from utils import input_date, input_int, input_str

DATA_PLACES = "data/places.json"
DATA_CATEGORIES = "data/categories.json"
DATA_EVENTS = "data/events.json"
DATA_REGISTRATIONS = "data/registrations.json"


def load_all_data() -> tuple[dict, dict, dict, list]:
    """Загрузить все данные проекта из JSON-файлов.

    Ключи словарей в JSON хранятся как строки, поэтому приводим
    их обратно к int.
    """
    places = load_json(DATA_PLACES, {})
    places = {int(key): value for key, value in places.items()}

    categories = load_json(DATA_CATEGORIES, {})
    categories = {int(key): value for key, value in categories.items()}

    events = load_json(DATA_EVENTS, {})
    events = {int(key): value for key, value in events.items()}

    registrations = load_json(DATA_REGISTRATIONS, [])

    return places, categories, events, registrations


def save_all_data(
    places: dict,
    categories: dict,
    events: dict,
    registrations: list,
) -> None:
    """Сохранить все данные проекта в JSON-файлы."""
    save_json(DATA_PLACES, places)
    save_json(DATA_CATEGORIES, categories)
    save_json(DATA_EVENTS, events)
    save_json(DATA_REGISTRATIONS, registrations)


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


def handle_find_place(places: dict) -> None:
    """Обработать поиск места по подстроке."""
    if not places:
        print("Мест пока нет.")
        return
    query = input_str("Подстрока названия или адреса: ")
    found = find_places(places, query)
    if not found:
        print("Ничего не найдено.")
        return
    for place in found:
        print(f"[{place['id']}] {place['name']} — "
              f"{place['address']}")


def handle_add_place(places: dict) -> None:
    """Обработать добавление места."""
    name = input_str("Название места: ")
    address = input_str("Адрес: ")
    place_id = add_place(places, name, address)
    print(f"Место добавлено, id={place_id}")


def handle_add_category(categories: dict) -> None:
    """Обработать добавление категории."""
    name = input_str("Название категории: ")
    description = input("Описание (необязательно): ").strip()
    category_id = add_category(categories, name, description)
    print(f"Категория добавлена, id={category_id}")


def handle_add_event(
    events: dict,
    places: dict,
    categories: dict,
) -> None:
    """Обработать добавление события."""
    if not places:
        print("Сначала добавьте хотя бы одно место.")
        return
    if not categories:
        print("Сначала добавьте хотя бы одну категорию.")
        return
    title = input_str("Название события: ")

    show_places(places)
    place_id = input_int("id места: ")
    if place_id not in places:
        print("Место с таким id не найдено.")
        return

    show_categories(categories)
    category_id = input_int("id категории: ")
    if category_id not in categories:
        print("Категория с таким id не найдена.")
        return

    iso_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    event_id = add_event(
        events,
        title,
        place_id,
        category_id,
        date.fromisoformat(iso_date),
    )
    print(f"Событие добавлено, id={event_id}")


def handle_find_event(events: dict) -> None:
    """Обработать поиск события по названию."""
    query = input_str("Подстрока названия: ")
    found = find_events(events, query)
    if not found:
        print("Ничего не найдено.")
        return
    for event in found:
        print(f"[{event['id']}] {event['title']} | "
              f"{event['event_date']}")


def handle_events_on_date(events: dict) -> None:
    """Показать события на выбранную дату."""
    iso_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    on_date = date.fromisoformat(iso_date)
    found = filter_events_by_date(events, on_date)
    if not found:
        print("На эту дату событий нет.")
        return
    for event in found:
        print(f"[{event['id']}] {event['title']} | "
              f"{get_event_status(on_date)}")


def handle_create_registration(
    registrations: list,
    events: dict,
) -> None:
    """Обработать создание регистрации на событие."""
    if not events:
        print("Событий пока нет.")
        return
    show_events(events)
    event_id = input_int("id события: ")
    if event_id not in events:
        print("Событие с таким id не найдено.")
        return
    user_name = input_str("Ваше имя: ")
    try:
        registration = create_registration(
            registrations, event_id, user_name
        )
        print(f"Регистрация создана, id={registration['id']}")
    except ValueError as error:
        print(f"Ошибка: {error}")


def handle_cancel_registration(registrations: list) -> None:
    """Обработать отмену регистрации."""
    if not registrations:
        print("Регистраций пока нет.")
        return
    show_registrations(registrations)
    registration_id = input_int("id регистрации: ")
    if cancel_registration(registrations, registration_id):
        print("Регистрация отменена.")
    else:
        print("Регистрация с таким id не найдена.")


def main() -> None:
    """Точка запуска приложения: меню и вызов функций проекта."""
    places, categories, events, registrations = load_all_data()

    while True:
        print_menu()
        choice = input_int("Выберите действие: ")

        if choice == 0:
            break
        elif choice == 1:
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
            handle_create_registration(registrations, events)
        elif choice == 11:
            show_registrations(registrations)
        elif choice == 12:
            handle_cancel_registration(registrations)
        else:
            print("Неизвестная команда, попробуйте снова.")

    save_all_data(places, categories, events, registrations)
    print("Данные сохранены. До свидания!")


if __name__ == "__main__":
    main()
