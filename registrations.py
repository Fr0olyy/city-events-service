"""Функции для работы с регистрациями на события."""


def is_registration_open(
    registrations: list[dict],
    event_id: int,
) -> bool:
    """Проверить, свободно ли ещё место на событие."""
    for registration in registrations:
        if registration["event_id"] == event_id:
            return False
    return True


def create_registration(
    registrations: list[dict],
    event_id: int,
    user_name: str,
) -> dict:
    """Создать регистрацию, если её ещё нет."""
    if not is_registration_open(registrations, event_id):
        raise ValueError(
            "Регистрация на это событие уже существует"
        )
    new_id = 1
    for registration in registrations:
        if registration["id"] >= new_id:
            new_id = registration["id"] + 1
    registration = {
        "id": new_id,
        "event_id": event_id,
        "user_name": user_name,
    }
    registrations.append(registration)
    return registration


def cancel_registration(
    registrations: list[dict],
    registration_id: int,
) -> bool:
    """Отменить регистрацию по id. True, если удалось."""
    for index, registration in enumerate(registrations):
        if registration["id"] == registration_id:
            registrations.pop(index)
            return True
    return False


def show_registrations(registrations: list[dict]) -> None:
    """Вывести список регистраций."""
    if not registrations:
        print("Регистраций пока нет.")
        return
    for registration in registrations:
        print(
            f"[{registration['id']}] событие="
            f"{registration['event_id']} "
            f"участник={registration['user_name']}"
        )
