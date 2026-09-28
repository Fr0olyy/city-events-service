"""Операции над регистрациями пользователей на события."""

from models import Event, Registration, User


def is_registration_open(
    registrations: list[Registration],
    event: Event | int,
) -> bool:
    """Проверить, нет ли активной регистрации на событие."""
    event_id = event.id if isinstance(event, Event) else event
    return not any(
        registration.event.id == event_id
        and not registration.is_cancelled
        for registration in registrations
    )


def create_registration(
    registrations: list[Registration],
    event: Event,
    user: User,
) -> Registration:
    """Создать регистрацию для объекта пользователя и события."""
    if not is_registration_open(registrations, event):
        raise ValueError("Регистрация на это событие уже существует")
    new_id = max(
        (registration.id for registration in registrations), default=0
    ) + 1
    registration = Registration(new_id, event, user)
    registrations.append(registration)
    return registration


def cancel_registration(
    registrations: list[Registration],
    registration_id: int,
) -> bool:
    """Отменить регистрацию по id, оставив её в истории."""
    for registration in registrations:
        if registration.id == registration_id and not registration.is_cancelled:
            registration.cancel()
            return True
    return False


def show_registrations(registrations: list[Registration]) -> None:
    """Вывести список регистраций."""
    if not registrations:
        print("Регистраций пока нет.")
        return
    for registration in registrations:
        print(registration)
