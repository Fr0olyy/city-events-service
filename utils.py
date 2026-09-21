"""Вспомогательные функции ввода с обработкой ошибок."""
from datetime import datetime


def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число, повторять при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить непустую строку, повторять при пустом вводе."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")


def input_date(prompt: str) -> str:
    """Запросить дату в формате ДД.ММ.ГГГГ, вернуть ISO-строку."""
    while True:
        raw = input(prompt)
        try:
            dt = datetime.strptime(raw, "%d.%m.%Y")
            return dt.date().isoformat()
        except ValueError:
            print("Ошибка: неверный формат. Ожидается ДД.ММ.ГГГГ.")
