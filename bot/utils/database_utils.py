import sqlite3
from bot.utils.court_parcer import parse_and_fill_database


def is_courts_table_empty():
    """Проверяет, пуста ли таблица courts."""
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM courts")
    result = cursor.fetchone()[0]
    conn.close()
    return result == 0

def initialize_database():
    """Создаёт таблицы regions и courts, если они ещё не существуют."""
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()

    # Создаём таблицы
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS regions (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region_id INTEGER,
            name TEXT,
            address TEXT,
            phone TEXT,
            email TEXT,
            url TEXT,
            FOREIGN KEY(region_id) REFERENCES regions(id)
        )
    """)
    conn.commit()
    conn.close()

    # Проверяем, нужно ли запустить парсинг
    if is_courts_table_empty():
        print("Таблица courts пуста. Запускается парсинг данных.")
        parse_and_fill_database()  # Вызов парсинга
    else:
        print("Таблица courts уже заполнена.")

def check_database():
    """Выводит примеры данных из базы."""
    conn = sqlite3.connect("courts.db")
    cursor = conn.cursor()

    # Проверить регионы
    regions = cursor.execute("SELECT * FROM regions LIMIT 5").fetchall()
    print("Пример данных из regions:", regions)

    # Проверить суды
    courts = cursor.execute("SELECT * FROM courts LIMIT 5").fetchall()
    print("Пример данных из courts:", courts)

    conn.close()
