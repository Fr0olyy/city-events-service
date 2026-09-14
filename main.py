import datetime

print("=== Сервис учета городских событий ===")

# Ввод данных
title = input("Название события: ").strip()
place = input("Место проведения: ").strip()
category = input("Категория (концерт/выставка/спорт): ").strip().lower()
date_str = input("Дата события (ГГГГ-ММ-ДД): ").strip()

# Преобразование типа
try:
    event_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
except ValueError:
    print("Ошибка: неверный формат даты. Ожидается ГГГГ-ММ-ДД.")
    exit(1)

today = datetime.date.today()

# Ветвление
if event_date < today:
    status = "уже прошло"
elif event_date == today:
    status = "сегодня"
else:
    days_left = (event_date - today).days
    status = f"через {days_left} дн."

if category not in ("концерт", "выставка", "спорт"):
    print("Предупреждение: неизвестная категория.")

print("\n--- Карточка события ---")
print(f"Название: {title}")
print(f"Место:    {place}")
print(f"Категория:{category}")
print(f"Дата:     {event_date}")
print(f"Статус:   {status}")