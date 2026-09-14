from datetime import date

# --- Данные о событии ---
event_title = "Городской джазовый концерт"
place_name = "Филармония"
category = "концерт"
event_date = date(2026, 9, 15)
is_registration_open = True
seats_left = 12


def get_event_status(event_date):
    """Определяет статус события относительно текущей даты.

    Сравнивает дату события с сегодняшней датой и возвращает
    строку с описанием: событие уже прошло, проходит сегодня
    или еще предстоит.
    """
    today = date.today()
    if event_date < today:
        return "Событие уже прошло"
    elif event_date == today:
        return "Событие проходит сегодня"
    else:
        days_left = (event_date - today).days
        return f"До события осталось дней: {days_left}"


def get_registration_status(is_registration_open, seats_left):
    """Возвращает статус регистрации на событие.

    Проверяет, открыта ли регистрация и остались ли свободные места.
    Если регистрация закрыта — сообщает об этом. Если мест нет —
    сообщает, что свободных мест не осталось.
    """
    if not is_registration_open:
        return "Регистрация закрыта"
    if seats_left <= 0:
        return "Свободных мест нет"
    return f"Регистрация открыта, свободных мест: {seats_left}"


def get_event_info(event_title, place_name, category, event_date):
    """Формирует текстовую карточку события.

    Собирает название, место, категорию и дату в одну строку,
    которую можно вывести пользователю.
    """
    return (f"{event_title} | {category} | {place_name} | {event_date}")


# --- Вывод информации о событии ---
print("=== Сервис учета городских событий ===")
print(get_event_info(event_title, place_name, category, event_date))
print(get_event_status(event_date))
print(get_registration_status(is_registration_open, seats_left))